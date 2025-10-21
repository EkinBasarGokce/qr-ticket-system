from django.urls import path
from . import views

urlpatterns = [
    path('event/<int:event_id>/', views.event_landing, name='event_landing'),
    path('ticket/<uuid:ticket_uuid>/', views.ticket_display, name='ticket_display'),
    path('ticket/<uuid:ticket_uuid>/download/', views.download_qr, name='download_qr'),
    path('scanner/', views.scanner_dashboard, name='scanner_dashboard'),
    path('api/validate-ticket/', views.validate_ticket, name='validate_ticket'),
]

