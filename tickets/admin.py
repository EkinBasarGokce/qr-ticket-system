from django.contrib import admin
from django.utils.html import format_html
from .models import Event, Ticket


class TicketInline(admin.TabularInline):
    """Inline display of tickets for an event"""
    model = Ticket
    extra = 0
    readonly_fields = ('unique_id', 'attendee_name', 'plus_ones', 'status', 'created_at', 'qr_code_preview')
    fields = ('attendee_name', 'plus_ones', 'status', 'created_at', 'qr_code_preview')
    can_delete = False
    
    def qr_code_preview(self, obj):
        if obj.qr_code:
            return format_html('<img src="{}" width="50" height="50" />', obj.qr_code.url)
        return "No QR Code"
    qr_code_preview.short_description = 'QR Code'


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    """Admin interface for Event model"""
    list_display = ('name', 'date_time', 'location', 'tickets_sold_display', 'max_tickets', 'tickets_available_display', 'created_at')
    list_filter = ('date_time', 'created_at')
    search_fields = ('name', 'location')
    readonly_fields = ('tickets_sold_display', 'tickets_available_display', 'created_at')
    inlines = [TicketInline]
    
    fieldsets = (
        ('Event Information', {
            'fields': ('name', 'date_time', 'location')
        }),
        ('Ticket Management', {
            'fields': ('max_tickets', 'tickets_sold_display', 'tickets_available_display')
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def tickets_sold_display(self, obj):
        """Display tickets sold with color coding"""
        sold = obj.tickets_sold()
        percentage = (sold / obj.max_tickets * 100) if obj.max_tickets > 0 else 0
        
        if percentage >= 100:
            color = 'red'
        elif percentage >= 80:
            color = 'orange'
        else:
            color = 'green'
        
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color, sold
        )
    tickets_sold_display.short_description = 'Tickets Sold'
    
    def tickets_available_display(self, obj):
        """Display available tickets"""
        available = obj.tickets_available()
        return format_html(
            '<span style="font-weight: bold;">{}</span>',
            available
        )
    tickets_available_display.short_description = 'Available'


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    """Admin interface for Ticket model"""
    list_display = ('attendee_name', 'event', 'plus_ones', 'total_attendees', 'status', 'created_at', 'qr_code_preview')
    list_filter = ('status', 'event', 'created_at')
    search_fields = ('attendee_name', 'unique_id', 'event__name')
    readonly_fields = ('unique_id', 'qr_code_preview', 'created_at', 'checked_in_at')
    
    fieldsets = (
        ('Ticket Information', {
            'fields': ('event', 'attendee_name', 'plus_ones', 'unique_id')
        }),
        ('Status', {
            'fields': ('status', 'checked_in_at')
        }),
        ('QR Code', {
            'fields': ('qr_code', 'qr_code_preview')
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def qr_code_preview(self, obj):
        """Display QR code preview"""
        if obj.qr_code:
            return format_html(
                '<img src="{}" width="150" height="150" />',
                obj.qr_code.url
            )
        return "No QR Code"
    qr_code_preview.short_description = 'QR Code Preview'
    
    def total_attendees(self, obj):
        """Display total attendees"""
        return obj.total_attendees()
    total_attendees.short_description = 'Total Attendees'

