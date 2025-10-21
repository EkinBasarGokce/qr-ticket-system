# Complete File Manifest

This document contains the complete content of every file in the QR Ticket System project.

---

## Configuration Files

### `requirements.txt`
```
Django==4.2.7
gunicorn==21.2.0
psycopg2-binary==2.9.9
dj-database-url==2.1.0
whitenoise==6.6.0
qrcode==7.4.2
Pillow==10.1.0
```

### `runtime.txt`
```
python-3.11.0
```

### `Procfile`
```
web: gunicorn qr_ticket_system.wsgi --log-file -
```

### `.gitignore`
```
*.pyc
__pycache__/
db.sqlite3
media/
staticfiles/
.env
venv/
*.log
```

---

## Project Settings: `qr_ticket_system/`

### `qr_ticket_system/settings.py`
See the file in the project directory. Key configurations:
- Database: SQLite (dev) / PostgreSQL (prod)
- Static files: WhiteNoise
- Media files: Local storage
- Security: Production-ready settings
- Localization: Turkish (tr)
- Timezone: Europe/Istanbul

### `qr_ticket_system/urls.py`
```python
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tickets.urls')),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

---

## Application: `tickets/`

### `tickets/models.py`
Contains two main models:
1. **Event**: Manages events with capacity tracking
2. **Ticket**: Manages individual tickets with QR codes

Key features:
- UUID-based unique identifiers
- Status tracking (unused/used)
- Plus-ones support
- Automatic QR code storage

### `tickets/admin.py`
Custom admin interface with:
- Inline ticket display
- Color-coded statistics
- QR code preview
- Advanced filtering
- Search functionality

### `tickets/views.py`
View functions:
- `event_landing()`: Public ticket creation
- `ticket_display()`: Show ticket with QR
- `download_qr()`: Download QR code
- `scanner_dashboard()`: Scanner interface
- `validate_ticket()`: API for validation
- `generate_qr_code()`: QR generation helper

### `tickets/forms.py`
```python
from django import forms
from .models import Ticket

class TicketCreationForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['attendee_name', 'plus_ones']
        widgets = {
            'attendee_name': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Adınız ve Soyadınız',
                'required': True
            }),
            'plus_ones': forms.NumberInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': '0',
                'min': '0',
                'value': '0',
                'required': True
            })
        }
        labels = {
            'attendee_name': 'Ad Soyad',
            'plus_ones': 'Kaç Kişi Getireceksiniz? (+1, +2, vb.)'
        }
    
    def clean_plus_ones(self):
        plus_ones = self.cleaned_data.get('plus_ones')
        if plus_ones < 0:
            raise forms.ValidationError('Plus ones cannot be negative.')
        return plus_ones
```

### `tickets/urls.py`
```python
from django.urls import path
from . import views

urlpatterns = [
    path('event/<int:event_id>/', views.event_landing, name='event_landing'),
    path('ticket/<uuid:ticket_uuid>/', views.ticket_display, name='ticket_display'),
    path('ticket/<uuid:ticket_uuid>/download/', views.download_qr, name='download_qr'),
    path('scanner/', views.scanner_dashboard, name='scanner_dashboard'),
    path('api/validate-ticket/', views.validate_ticket, name='validate_ticket'),
]
```

---

## Templates

### Template Structure
```
tickets/templates/
├── tickets/
│   ├── base.html           # Base template with Bootstrap 5
│   ├── event_landing.html  # Public ticket creation page
│   ├── ticket_display.html # Ticket display with QR code
│   └── scanner_dashboard.html # QR scanner interface
└── registration/
    └── login.html          # Login page for scanners
```

### Key Template Features

**base.html:**
- Bootstrap 5 integration
- Gradient background design
- Responsive navigation
- Message display system
- Mobile-friendly layout

**event_landing.html:**
- Event information display
- Capacity tracking
- Ticket creation form
- Sold-out handling
- Input validation

**ticket_display.html:**
- QR code display
- Download functionality
- Event details
- Attendee information
- Security warnings

**scanner_dashboard.html:**
- html5-qrcode integration
- Real-time camera scanning
- Ticket validation display
- AJAX API calls
- Status indicators
- Error handling

**login.html:**
- Clean, centered design
- Bootstrap form styling
- Error messages
- Redirect handling

---

## Documentation Files

### README.md
Comprehensive documentation including:
- Feature overview
- Technology stack
- Installation instructions
- Usage guide
- Model descriptions
- API endpoints
- Security features
- Troubleshooting

### DEPLOYMENT_GUIDE.md
Step-by-step Heroku deployment:
- Prerequisites
- Configuration
- Database setup
- Environment variables
- AWS S3 integration
- Custom domains
- Monitoring
- Scaling options

### QUICK_START.md
5-minute quick start guide:
- Installation steps
- Default credentials
- Testing workflow
- Mobile testing
- Customization tips
- Troubleshooting
- Pro tips

### PROJECT_STRUCTURE.md
Complete project overview:
- Directory structure
- File descriptions
- Implementation details
- Database schema
- API documentation
- Testing checklist
- Maintenance tasks
- Future enhancements

---

## Default Credentials

### Admin User
- Username: `admin`
- Password: `admin123`
- Access: Full Django admin

### Scanner User
- Username: `scanner`
- Password: `scanner123`
- Access: Scanner dashboard only

### Sample Event
- Name: Tech Conference 2025
- Location: Istanbul Convention Center
- Max Tickets: 100
- ID: 1

---

## URLs Reference

### Public URLs (No Login Required)
- `/event/<event_id>/` - Event landing page
- `/ticket/<ticket_uuid>/` - Ticket display
- `/ticket/<ticket_uuid>/download/` - Download QR code

### Protected URLs (Login Required)
- `/admin/` - Django admin panel
- `/scanner/` - Scanner dashboard
- `/api/validate-ticket/` - Ticket validation API

### Authentication URLs
- `/login/` - Login page
- `/logout/` - Logout

---

## API Documentation

### POST /api/validate-ticket/

**Authentication:** Required (Login)

**Parameters:**
- `ticket_uuid` (string): UUID of the ticket to validate

**Response Format:**
```json
{
    "success": boolean,
    "message": string,
    "ticket": {
        "attendee_name": string,
        "event_name": string,
        "event_date": string,
        "event_location": string,
        "plus_ones": integer,
        "total_attendees": integer,
        "status": string,
        "checked_in_at": string
    }
}
```

**Success Response:**
```json
{
    "success": true,
    "message": "Bilet başarıyla onaylandı!",
    "ticket": {
        "attendee_name": "John Doe",
        "event_name": "Tech Conference 2025",
        "event_date": "2025-11-20 14:00",
        "event_location": "Istanbul Convention Center",
        "plus_ones": 2,
        "total_attendees": 3,
        "status": "Checked-In",
        "checked_in_at": "2025-10-21 10:30:00"
    }
}
```

**Error Response (Already Used):**
```json
{
    "success": false,
    "message": "Bu bilet zaten kullanılmış!",
    "ticket": {
        "attendee_name": "John Doe",
        "event_name": "Tech Conference 2025",
        "plus_ones": 2,
        "status": "Checked-In",
        "checked_in_at": "2025-10-21 10:30:00"
    }
}
```

**Error Response (Invalid):**
```json
{
    "success": false,
    "message": "Geçersiz bilet!"
}
```

---

## Database Models

### Event Model Fields
- `id`: Auto-incrementing primary key
- `name`: CharField(max_length=200)
- `date_time`: DateTimeField
- `location`: CharField(max_length=300)
- `max_tickets`: IntegerField(default=100)
- `created_at`: DateTimeField(auto_now_add=True)

### Event Model Methods
- `tickets_sold()`: Returns total tickets sold including plus ones
- `tickets_available()`: Returns remaining tickets
- `is_sold_out()`: Returns boolean if event is sold out

### Ticket Model Fields
- `id`: Auto-incrementing primary key
- `event`: ForeignKey(Event, on_delete=CASCADE)
- `attendee_name`: CharField(max_length=200)
- `plus_ones`: IntegerField(default=0)
- `unique_id`: UUIDField(default=uuid4, unique=True)
- `status`: CharField(max_length=10, choices=['unused', 'used'])
- `qr_code`: ImageField(upload_to='qr_codes/')
- `created_at`: DateTimeField(auto_now_add=True)
- `checked_in_at`: DateTimeField(blank=True, null=True)

### Ticket Model Methods
- `total_attendees()`: Returns 1 + plus_ones
- `check_in()`: Marks ticket as used and sets checked_in_at

---

## Installation Commands

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Create scanner user
python manage.py shell
>>> from django.contrib.auth.models import User
>>> User.objects.create_user('scanner', 'scanner@example.com', 'scanner123')

# Run server
python manage.py runserver
```

### Heroku Deployment
```bash
# Login to Heroku
heroku login

# Create app
heroku create your-app-name

# Set environment variables
heroku config:set SECRET_KEY='your-secret-key'
heroku config:set DEBUG=False

# Add PostgreSQL
heroku addons:create heroku-postgresql:essential-0

# Deploy
git push heroku main

# Run migrations
heroku run python manage.py migrate

# Create superuser
heroku run python manage.py createsuperuser
```

---

## Testing Workflow

### 1. Create Event (Admin)
1. Go to `/admin/`
2. Login with admin credentials
3. Click "Events" → "Add Event"
4. Fill in details and save

### 2. Create Ticket (Attendee)
1. Go to `/event/1/`
2. Enter name and plus ones
3. Click "Davetiyemi Oluştur"
4. Download QR code

### 3. Validate Ticket (Scanner)
1. Go to `/login/`
2. Login with scanner credentials
3. Allow camera access
4. Scan QR code
5. Verify check-in

---

## File Locations

### Python Files
- `manage.py` - Django management script
- `qr_ticket_system/settings.py` - Settings
- `qr_ticket_system/urls.py` - URL routing
- `qr_ticket_system/wsgi.py` - WSGI config
- `tickets/models.py` - Database models
- `tickets/admin.py` - Admin customization
- `tickets/views.py` - View functions
- `tickets/forms.py` - Form definitions
- `tickets/urls.py` - App URLs

### Template Files
- `tickets/templates/tickets/base.html`
- `tickets/templates/tickets/event_landing.html`
- `tickets/templates/tickets/ticket_display.html`
- `tickets/templates/tickets/scanner_dashboard.html`
- `tickets/templates/registration/login.html`

### Configuration Files
- `requirements.txt` - Python dependencies
- `runtime.txt` - Python version
- `Procfile` - Heroku process
- `.gitignore` - Git ignore rules

### Documentation Files
- `README.md` - Main documentation
- `DEPLOYMENT_GUIDE.md` - Deployment instructions
- `QUICK_START.md` - Quick start guide
- `PROJECT_STRUCTURE.md` - Structure overview
- `FILE_MANIFEST.md` - This file

---

## Dependencies

### Python Packages
- Django 4.2.7 - Web framework
- gunicorn 21.2.0 - WSGI server
- psycopg2-binary 2.9.9 - PostgreSQL adapter
- dj-database-url 2.1.0 - Database URL parser
- whitenoise 6.6.0 - Static file serving
- qrcode 7.4.2 - QR code generation
- Pillow 10.1.0 - Image processing

### Frontend Libraries (CDN)
- Bootstrap 5.3.2 - CSS framework
- Bootstrap Icons 1.11.1 - Icon library
- html5-qrcode 2.3.8 - QR code scanner

---

## Security Considerations

### Production Settings
- DEBUG=False
- SECRET_KEY from environment
- ALLOWED_HOSTS configured
- HTTPS redirect enabled
- Secure cookies enabled
- CSRF protection enabled
- XSS protection enabled

### Authentication
- Django's built-in auth system
- Password validation
- Login required for scanner
- Admin-only event management
- Public ticket creation

### Data Protection
- UUID-based ticket IDs
- Single-use tickets
- Check-in timestamp tracking
- Status validation

---

## Maintenance

### Regular Tasks
- Monitor disk usage
- Review old events
- Backup database
- Update dependencies
- Check error logs

### Security Updates
- Rotate SECRET_KEY
- Update Django
- Update dependencies
- Review permissions
- Monitor logins

---

## Support Resources

### Documentation
- Django: https://docs.djangoproject.com/
- Bootstrap: https://getbootstrap.com/docs/
- html5-qrcode: https://github.com/mebjas/html5-qrcode
- Heroku: https://devcenter.heroku.com/

### Project Files
- README.md - Full documentation
- DEPLOYMENT_GUIDE.md - Deployment steps
- QUICK_START.md - Quick start
- PROJECT_STRUCTURE.md - Code structure

---

End of File Manifest

