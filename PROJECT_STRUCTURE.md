# Complete Project Structure and File Contents

This document provides a complete overview of all files in the QR Ticket System project.

## Directory Structure

```
qr_ticket_system_project/
├── .gitignore
├── Procfile
├── README.md
├── DEPLOYMENT_GUIDE.md
├── PROJECT_STRUCTURE.md
├── requirements.txt
├── runtime.txt
├── manage.py
├── db.sqlite3 (generated)
├── media/ (generated)
│   └── qr_codes/
├── staticfiles/ (generated)
├── qr_ticket_system/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
└── tickets/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── forms.py
    ├── models.py
    ├── urls.py
    ├── views.py
    ├── migrations/
    │   ├── __init__.py
    │   └── 0001_initial.py
    └── templates/
        ├── tickets/
        │   ├── base.html
        │   ├── event_landing.html
        │   ├── ticket_display.html
        │   └── scanner_dashboard.html
        └── registration/
            └── login.html
```

## File Descriptions

### Root Configuration Files

#### `.gitignore`
Specifies files and directories to be ignored by Git version control.

#### `Procfile`
Tells Heroku how to run the application.
```
web: gunicorn qr_ticket_system.wsgi --log-file -
```

#### `requirements.txt`
Lists all Python dependencies required by the project.

#### `runtime.txt`
Specifies the Python version for Heroku.
```
python-3.11.0
```

#### `manage.py`
Django's command-line utility for administrative tasks (auto-generated).

### Project Package: `qr_ticket_system/`

#### `settings.py`
Main Django settings file with production-ready configuration:
- Database configuration (SQLite for dev, PostgreSQL for production)
- Static files configuration with WhiteNoise
- Media files configuration
- Security settings
- Authentication settings
- Turkish localization

#### `urls.py`
Main URL configuration:
- Admin interface
- Tickets app URLs
- Authentication URLs (login/logout)
- Media file serving in development

#### `wsgi.py`
WSGI configuration for deployment (auto-generated).

#### `asgi.py`
ASGI configuration for async support (auto-generated).

### Application Package: `tickets/`

#### `models.py`
Defines the database models:

**Event Model:**
- name: CharField
- date_time: DateTimeField
- location: CharField
- max_tickets: IntegerField
- created_at: DateTimeField
- Methods: tickets_sold(), tickets_available(), is_sold_out()

**Ticket Model:**
- event: ForeignKey to Event
- attendee_name: CharField
- plus_ones: IntegerField
- unique_id: UUIDField (auto-generated)
- status: CharField (choices: 'unused', 'used')
- qr_code: ImageField
- created_at: DateTimeField
- checked_in_at: DateTimeField
- Methods: total_attendees(), check_in()

#### `admin.py`
Django admin customization:
- EventAdmin: Custom list display, inline tickets, color-coded ticket counts
- TicketAdmin: Custom list display, QR code preview, filtering
- TicketInline: Inline display of tickets within event admin

#### `views.py`
View functions:
- `event_landing()`: Public page for ticket creation
- `ticket_display()`: Display ticket with QR code
- `download_qr()`: Download QR code as PNG
- `scanner_dashboard()`: Scanner interface (login required)
- `validate_ticket()`: API endpoint for ticket validation (login required)
- `generate_qr_code()`: Helper function to generate QR codes

#### `forms.py`
Form definitions:
- TicketCreationForm: Form for creating tickets with validation

#### `urls.py`
URL patterns for the tickets app:
- `/event/<event_id>/` - Event landing page
- `/ticket/<ticket_uuid>/` - Ticket display
- `/ticket/<ticket_uuid>/download/` - Download QR code
- `/scanner/` - Scanner dashboard
- `/api/validate-ticket/` - Validation API

#### `apps.py`
App configuration (auto-generated).

### Templates: `tickets/templates/`

#### `tickets/base.html`
Base template with:
- Bootstrap 5 integration
- Responsive navigation bar
- Gradient background design
- Message display system
- Block structure for content and scripts

#### `tickets/event_landing.html`
Event landing page featuring:
- Event information display
- Ticket availability counter
- Ticket creation form
- Sold-out handling
- Responsive design

#### `tickets/ticket_display.html`
Ticket display page with:
- QR code display
- Download button
- Event details
- Attendee information
- Security warning

#### `tickets/scanner_dashboard.html`
Scanner dashboard featuring:
- html5-qrcode integration
- Real-time QR scanning
- Ticket validation display
- Check-in status
- Error handling
- Responsive camera interface

#### `registration/login.html`
Login page with:
- Clean, centered design
- Bootstrap form styling
- Error message display
- Redirect handling

## Key Features Implementation

### 1. QR Code Generation
- Uses `qrcode` library with Pillow
- Generates unique UUID for each ticket
- Saves QR code as PNG image
- Associates image with ticket model

### 2. QR Code Scanning
- Uses html5-qrcode JavaScript library
- Accesses device camera
- Decodes QR code to UUID
- Validates via AJAX API call

### 3. Ticket Validation
- CSRF-protected API endpoint
- Checks ticket existence
- Prevents duplicate check-ins
- Returns detailed ticket information
- Updates ticket status atomically

### 4. User Authentication
- Django's built-in auth system
- Three user types: Admin, Scanner, Attendee
- Login required for scanner functionality
- No login required for ticket creation

### 5. Admin Interface
- Custom admin classes
- Inline ticket display
- Color-coded statistics
- QR code preview
- Filtering and search

### 6. Responsive Design
- Bootstrap 5 framework
- Mobile-first approach
- Works on phones, tablets, and desktops
- Camera access on mobile devices

### 7. Production Ready
- WhiteNoise for static files
- PostgreSQL support
- Environment variable configuration
- Security settings for production
- Gunicorn WSGI server

## Database Schema

### Event Table
```sql
CREATE TABLE tickets_event (
    id INTEGER PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    date_time DATETIME NOT NULL,
    location VARCHAR(300) NOT NULL,
    max_tickets INTEGER NOT NULL,
    created_at DATETIME NOT NULL
);
```

### Ticket Table
```sql
CREATE TABLE tickets_ticket (
    id INTEGER PRIMARY KEY,
    event_id INTEGER NOT NULL,
    attendee_name VARCHAR(200) NOT NULL,
    plus_ones INTEGER NOT NULL,
    unique_id UUID NOT NULL UNIQUE,
    status VARCHAR(10) NOT NULL,
    qr_code VARCHAR(100),
    created_at DATETIME NOT NULL,
    checked_in_at DATETIME,
    FOREIGN KEY (event_id) REFERENCES tickets_event(id)
);
```

## API Endpoints

### POST /api/validate-ticket/
**Authentication:** Required (Scanner user)

**Request:**
```
ticket_uuid=<uuid>
```

**Response (Success):**
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

**Response (Already Used):**
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

**Response (Invalid):**
```json
{
    "success": false,
    "message": "Geçersiz bilet!"
}
```

## Environment Variables

### Required for Production

- `SECRET_KEY`: Django secret key
- `DEBUG`: Set to 'False' for production
- `DATABASE_URL`: PostgreSQL connection string (auto-set by Heroku)

### Optional for AWS S3

- `AWS_ACCESS_KEY_ID`: AWS access key
- `AWS_SECRET_ACCESS_KEY`: AWS secret key
- `AWS_STORAGE_BUCKET_NAME`: S3 bucket name

## Testing Checklist

### Local Testing
- [ ] Admin can log in and create events
- [ ] Attendee can create tickets without login
- [ ] QR codes are generated and displayed
- [ ] QR codes can be downloaded
- [ ] Scanner can log in
- [ ] Scanner can scan QR codes
- [ ] Tickets are validated correctly
- [ ] Duplicate check-ins are prevented
- [ ] Capacity limits are enforced

### Production Testing
- [ ] HTTPS is enabled
- [ ] Static files load correctly
- [ ] Media files are accessible
- [ ] Database connections work
- [ ] Environment variables are set
- [ ] Camera access works on mobile
- [ ] QR scanning works on mobile
- [ ] All pages are responsive

## Maintenance Tasks

### Regular Tasks
- Monitor disk usage (media files)
- Review and delete old events
- Backup database regularly
- Update dependencies periodically
- Monitor error logs

### Security Tasks
- Rotate SECRET_KEY periodically
- Update Django and dependencies
- Review user permissions
- Monitor failed login attempts
- Check for security advisories

## Future Enhancements

### Potential Features
- Email ticket delivery
- SMS notifications
- Multiple QR code formats
- Ticket transfer functionality
- Analytics dashboard
- Export attendee lists
- Bulk ticket creation
- Event categories
- Ticket pricing
- Payment integration
- Multi-language support
- Mobile app

### Performance Optimizations
- Database query optimization
- Caching implementation
- CDN for static files
- Image optimization
- Async task processing
- Load balancing

## License and Credits

This project uses the following open-source libraries:
- Django (BSD License)
- Bootstrap (MIT License)
- html5-qrcode (MIT License)
- qrcode (BSD License)
- Pillow (PIL License)
- WhiteNoise (MIT License)
- Gunicorn (MIT License)

