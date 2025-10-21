import os
import qrcode
from io import BytesIO
from django.core.files import File
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import Event, Ticket
from .forms import TicketCreationForm


def event_landing(request, event_id):
    """Public landing page for event ticket creation"""
    event = get_object_or_404(Event, id=event_id)
    
    if request.method == 'POST':
        form = TicketCreationForm(request.POST)
        if form.is_valid():
            # Check if event is sold out
            requested_tickets = 1 + form.cleaned_data['plus_ones']
            if event.tickets_sold() + requested_tickets > event.max_tickets:
                messages.error(request, 'Üzgünüz, yeterli bilet kalmadı!')
                return redirect('event_landing', event_id=event_id)
            
            # Create ticket
            ticket = form.save(commit=False)
            ticket.event = event
            ticket.save()
            
            # Generate QR code
            generate_qr_code(ticket)
            
            messages.success(request, 'Davetiyeniz başarıyla oluşturuldu!')
            return redirect('ticket_display', ticket_uuid=ticket.unique_id)
    else:
        form = TicketCreationForm()
    
    context = {
        'event': event,
        'form': form,
        'tickets_sold': event.tickets_sold(),
        'tickets_available': event.tickets_available(),
        'is_sold_out': event.is_sold_out()
    }
    return render(request, 'tickets/event_landing.html', context)


def ticket_display(request, ticket_uuid):
    """Display ticket with QR code"""
    ticket = get_object_or_404(Ticket, unique_id=ticket_uuid)
    
    context = {
        'ticket': ticket,
    }
    return render(request, 'tickets/ticket_display.html', context)


def download_qr(request, ticket_uuid):
    """Download QR code as PNG file"""
    ticket = get_object_or_404(Ticket, unique_id=ticket_uuid)
    
    if ticket.qr_code:
        response = HttpResponse(ticket.qr_code.read(), content_type='image/png')
        response['Content-Disposition'] = f'attachment; filename="ticket_{ticket.unique_id}.png"'
        return response
    
    return HttpResponse('QR code not found', status=404)


@login_required
def scanner_dashboard(request):
    """Scanner dashboard for checking in tickets"""
    return render(request, 'tickets/scanner_dashboard.html')


@login_required
@csrf_exempt
def validate_ticket(request):
    """API endpoint to validate and check-in tickets"""
    if request.method == 'POST':
        ticket_uuid = request.POST.get('ticket_uuid', '').strip()
        
        try:
            ticket = Ticket.objects.get(unique_id=ticket_uuid)
            
            if ticket.status == 'used':
                return JsonResponse({
                    'success': False,
                    'message': 'Bu bilet zaten kullanılmış!',
                    'ticket': {
                        'attendee_name': ticket.attendee_name,
                        'event_name': ticket.event.name,
                        'plus_ones': ticket.plus_ones,
                        'status': ticket.get_status_display(),
                        'checked_in_at': ticket.checked_in_at.strftime('%Y-%m-%d %H:%M:%S') if ticket.checked_in_at else None
                    }
                })
            
            # Check in the ticket
            ticket.check_in()
            
            return JsonResponse({
                'success': True,
                'message': 'Bilet başarıyla onaylandı!',
                'ticket': {
                    'attendee_name': ticket.attendee_name,
                    'event_name': ticket.event.name,
                    'event_date': ticket.event.date_time.strftime('%Y-%m-%d %H:%M'),
                    'event_location': ticket.event.location,
                    'plus_ones': ticket.plus_ones,
                    'total_attendees': ticket.total_attendees(),
                    'status': ticket.get_status_display(),
                    'checked_in_at': ticket.checked_in_at.strftime('%Y-%m-%d %H:%M:%S') if ticket.checked_in_at else None
                }
            })
            
        except Ticket.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Geçersiz bilet!'
            })
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})


def generate_qr_code(ticket):
    """Generate QR code for a ticket"""
    # Create QR code with ticket UUID
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(str(ticket.unique_id))
    qr.make(fit=True)
    
    # Create image
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Save to BytesIO
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    
    # Save to ticket model
    filename = f'ticket_{ticket.unique_id}.png'
    ticket.qr_code.save(filename, File(buffer), save=True)
    buffer.close()

