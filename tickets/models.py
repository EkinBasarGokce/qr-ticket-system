import uuid
from django.db import models
from django.utils import timezone


class Event(models.Model):
    """Event model for managing ticketed events"""
    name = models.CharField(max_length=200)
    date_time = models.DateTimeField()
    location = models.CharField(max_length=300)
    max_tickets = models.IntegerField(default=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date_time']
    
    def __str__(self):
        return f"{self.name} - {self.date_time.strftime('%Y-%m-%d %H:%M')}"
    
    def tickets_sold(self):
        """Calculate total tickets sold including plus ones"""
        tickets = self.ticket_set.all()
        return sum(1 + ticket.plus_ones for ticket in tickets)
    
    def tickets_available(self):
        """Calculate remaining tickets"""
        return max(0, self.max_tickets - self.tickets_sold())
    
    def is_sold_out(self):
        """Check if event is sold out"""
        return self.tickets_sold() >= self.max_tickets


class Ticket(models.Model):
    """Ticket model for event attendees"""
    STATUS_CHOICES = [
        ('unused', 'Not Used'),
        ('used', 'Checked-In'),
    ]
    
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    attendee_name = models.CharField(max_length=200)
    plus_ones = models.IntegerField(default=0)
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='unused')
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    checked_in_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.attendee_name} - {self.event.name}"
    
    def total_attendees(self):
        """Total number of people including the ticket holder"""
        return 1 + self.plus_ones
    
    def check_in(self):
        """Mark ticket as used"""
        if self.status == 'unused':
            self.status = 'used'
            self.checked_in_at = timezone.now()
            self.save()
            return True
        return False

