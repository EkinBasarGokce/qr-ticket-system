# QR Ticket System

A complete Django-based digital ticketing system with QR code generation and validation functionality. This system allows event organizers to create events, attendees to generate tickets, and scanners to validate tickets at the venue.

## Features

### User Types
- **Admin**: Full access to Django admin for event management
- **Scanner**: Can log in to scan and validate QR codes
- **Attendee**: Public access to create tickets (no login required)

### Core Functionality
- Event creation and management
- Ticket generation with unique QR codes
- Real-time QR code scanning and validation
- Ticket download functionality
- Capacity management and sold-out tracking
- Check-in status tracking

## Technology Stack

- **Backend**: Django 4.2.7
- **Database**: PostgreSQL (production) / SQLite (development)
- **QR Code**: qrcode + Pillow
- **Frontend**: Bootstrap 5
- **QR Scanner**: html5-qrcode
- **Deployment**: Heroku with Gunicorn
- **Static Files**: WhiteNoise

## Project Structure

```
qr_ticket_system_project/
├── manage.py
├── requirements.txt
├── runtime.txt
├── Procfile
├── README.md
├── qr_ticket_system/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
└── tickets/
    ├── __init__.py
    ├── models.py
    ├── admin.py
    ├── views.py
    ├── urls.py
    ├── forms.py
    ├── apps.py
    └── templates/
        ├── tickets/
        │   ├── base.html
        │   ├── event_landing.html
        │   ├── ticket_display.html
        │   └── scanner_dashboard.html
        └── registration/
            └── login.html
```

## Local Development Setup

### Prerequisites
- Python 3.11+
- pip

### Installation

1. **Clone or create the project directory**
   ```bash
   cd qr_ticket_system_project
   ```

2. **Create and activate virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser (Admin)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Create scanner user**
   ```bash
   python manage.py shell
   ```
   Then in the Python shell:
   ```python
   from django.contrib.auth.models import User
   User.objects.create_user(username='scanner', password='scanner123')
   exit()
   ```

7. **Run development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Admin panel: http://localhost:8000/admin/
   - Scanner login: http://localhost:8000/login/
   - Event landing: http://localhost:8000/event/1/ (after creating an event)

## Heroku Deployment

### Prerequisites
- Heroku CLI installed
- Git installed
- Heroku account

### Deployment Steps

1. **Initialize Git repository**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   ```

2. **Create Heroku app**
   ```bash
   heroku create your-app-name
   ```

3. **Set environment variables**
   ```bash
   heroku config:set SECRET_KEY='your-secret-key-here'
   heroku config:set DEBUG=False
   ```

4. **Add PostgreSQL addon**
   ```bash
   heroku addons:create heroku-postgresql:mini
   ```

5. **Deploy to Heroku**
   ```bash
   git push heroku main
   ```

6. **Run migrations on Heroku**
   ```bash
   heroku run python manage.py migrate
   ```

7. **Create superuser on Heroku**
   ```bash
   heroku run python manage.py createsuperuser
   ```

8. **Create scanner user on Heroku**
   ```bash
   heroku run python manage.py shell
   ```
   Then create the scanner user as shown in local setup.

9. **Open your app**
   ```bash
   heroku open
   ```

## Usage Guide

### For Admins

1. Log in to the admin panel at `/admin/`
2. Create events with the following information:
   - Event name
   - Date and time
   - Location
   - Maximum tickets
3. View ticket sales and attendee lists for each event
4. Monitor check-in status

### For Attendees

1. Visit the event landing page: `/event/<event_id>/`
2. Enter your full name
3. Specify how many additional people you're bringing (+1, +2, etc.)
4. Click "Davetiyemi Oluştur" (Create My Ticket)
5. Your ticket with QR code will be displayed
6. Download or screenshot the QR code

### For Scanners

1. Log in at `/login/` with scanner credentials
2. Allow camera access when prompted
3. Point the camera at the ticket's QR code
4. The system will automatically:
   - Validate the ticket
   - Display attendee information
   - Mark the ticket as "used"
   - Prevent duplicate check-ins

## Models

### Event Model
- `name`: Event name
- `date_time`: Event date and time
- `location`: Event location
- `max_tickets`: Maximum number of tickets
- `created_at`: Creation timestamp

### Ticket Model
- `event`: Foreign key to Event
- `attendee_name`: Name of the ticket holder
- `plus_ones`: Number of additional attendees
- `unique_id`: UUID for QR code
- `status`: 'unused' or 'used'
- `qr_code`: Image file of the QR code
- `created_at`: Creation timestamp
- `checked_in_at`: Check-in timestamp

## API Endpoints

### Public Endpoints
- `GET /event/<event_id>/` - Event landing page
- `GET /ticket/<ticket_uuid>/` - Ticket display page
- `GET /ticket/<ticket_uuid>/download/` - Download QR code

### Protected Endpoints (Login Required)
- `GET /scanner/` - Scanner dashboard
- `POST /api/validate-ticket/` - Validate and check-in ticket

## Security Features

- CSRF protection on all forms
- Login required for scanner functionality
- Unique UUID for each ticket
- Single-use ticket validation
- SSL redirect in production
- Secure cookies in production

## Media Files Note

On Heroku's ephemeral filesystem, uploaded QR code images will be lost on dyno restart. For production use, consider:
- Using AWS S3 for media storage
- Implementing django-storages
- Or regenerating QR codes on-the-fly

For initial deployment and testing, the current setup works fine.

## Troubleshooting

### QR codes not displaying
- Check that MEDIA_URL and MEDIA_ROOT are correctly configured
- Ensure the media directory exists and has write permissions
- Verify that static files are being served correctly

### Scanner not working
- Ensure HTTPS is enabled (required for camera access)
- Check browser permissions for camera access
- Verify that the scanner user has proper authentication

### Database issues on Heroku
- Ensure DATABASE_URL is set correctly
- Run migrations: `heroku run python manage.py migrate`
- Check logs: `heroku logs --tail`

## License

This project is provided as-is for educational and commercial use.

## Support

For issues and questions, please refer to the Django documentation or create an issue in the project repository.

