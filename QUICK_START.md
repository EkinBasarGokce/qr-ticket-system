# Quick Start Guide

## 🚀 Get Started in 5 Minutes

This guide will help you get the QR Ticket System running locally in just a few steps.

## Prerequisites

- Python 3.11+ installed
- pip package manager
- Basic terminal/command line knowledge

## Step 1: Extract the Project

If you have the archive file:
```bash
tar -xzf qr_ticket_system_complete.tar.gz
cd qr_ticket_system_project
```

If you already have the project folder:
```bash
cd qr_ticket_system_project
```

## Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- Django 4.2.7
- gunicorn
- psycopg2-binary
- dj-database-url
- whitenoise
- qrcode
- Pillow

## Step 3: Run the Server

The database is already set up with migrations applied, so you can start immediately:

```bash
python manage.py runserver
```

You should see:
```
Starting development server at http://127.0.0.1:8000/
```

## Step 4: Access the Application

### 🎫 Create a Ticket (No Login Required)

Open your browser and go to:
```
http://localhost:8000/event/1/
```

1. Enter your name
2. Enter number of plus ones (e.g., 0, 1, 2)
3. Click "Davetiyemi Oluştur"
4. Your ticket with QR code will be displayed
5. Download or screenshot the QR code

### 👨‍💼 Admin Panel

Go to:
```
http://localhost:8000/admin/
```

**Login credentials:**
- Username: `admin`
- Password: `admin123`

**What you can do:**
- Create new events
- View all tickets
- See ticket sales statistics
- Manage users
- View QR codes

### 📱 Scanner Dashboard

Go to:
```
http://localhost:8000/login/
```

**Login credentials:**
- Username: `scanner`
- Password: `scanner123`

After login, you'll be redirected to the scanner dashboard.

**What you can do:**
- Scan QR codes using your device camera
- Validate tickets
- Check-in attendees
- View ticket details

## Step 5: Test the Full Flow

### Complete Workflow Test:

1. **Create an Event (Admin)**
   - Go to http://localhost:8000/admin/
   - Login as admin
   - Click "Events" → "Add Event"
   - Fill in event details
   - Save

2. **Generate a Ticket (Attendee)**
   - Go to http://localhost:8000/event/1/ (or your event ID)
   - Enter name and plus ones
   - Submit form
   - Download QR code

3. **Scan the Ticket (Scanner)**
   - Go to http://localhost:8000/login/
   - Login as scanner
   - Allow camera access
   - Point camera at QR code
   - Verify check-in works

## 📱 Testing on Mobile

### Option 1: Using ngrok (Recommended)

Install ngrok:
```bash
# Download from https://ngrok.com/download
# Or use package manager
brew install ngrok  # macOS
```

Run ngrok:
```bash
ngrok http 8000
```

You'll get a public URL like: `https://abc123.ngrok.io`

Access from your phone:
```
https://abc123.ngrok.io/event/1/
```

### Option 2: Local Network

Find your local IP:
```bash
# On macOS/Linux
ifconfig | grep "inet "

# On Windows
ipconfig
```

Update `settings.py`:
```python
ALLOWED_HOSTS = ['*']  # Already set
```

Access from your phone (same WiFi):
```
http://YOUR_LOCAL_IP:8000/event/1/
```

## 🎨 Customization

### Change Event Details

Edit in admin panel or via shell:
```bash
python manage.py shell
```

```python
from tickets.models import Event
event = Event.objects.get(id=1)
event.name = "My Custom Event"
event.location = "My Venue"
event.max_tickets = 200
event.save()
```

### Change Admin Password

```bash
python manage.py changepassword admin
```

### Create Additional Scanner Users

```bash
python manage.py shell
```

```python
from django.contrib.auth.models import User
User.objects.create_user('scanner2', 'scanner2@example.com', 'password123')
```

### Customize Colors and Styling

Edit `tickets/templates/tickets/base.html`:
- Change gradient colors in the `<style>` section
- Modify Bootstrap classes
- Add custom CSS

## 🐛 Troubleshooting

### Port 8000 Already in Use

Use a different port:
```bash
python manage.py runserver 8080
```

### Camera Not Working

Requirements for camera access:
- HTTPS connection (use ngrok)
- Browser permissions granted
- Camera not in use by another app

### QR Codes Not Displaying

Check media directory exists:
```bash
mkdir -p media/qr_codes
```

Ensure media files are served (already configured in `urls.py`).

### Static Files Not Loading

Collect static files:
```bash
python manage.py collectstatic --noinput
```

### Database Errors

Reset database:
```bash
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

## 📚 Next Steps

### For Development

1. **Read the full README.md** for detailed documentation
2. **Check DEPLOYMENT_GUIDE.md** for Heroku deployment
3. **Review PROJECT_STRUCTURE.md** to understand the codebase
4. **Customize templates** in `tickets/templates/`
5. **Modify models** in `tickets/models.py`
6. **Add features** in `tickets/views.py`

### For Production

1. **Follow DEPLOYMENT_GUIDE.md** for Heroku setup
2. **Set up AWS S3** for media files (recommended)
3. **Configure custom domain**
4. **Set up SSL certificate** (automatic on Heroku)
5. **Enable database backups**
6. **Set up monitoring and logging**

## 🎯 Common Use Cases

### Corporate Events
- Set max_tickets to venue capacity
- Create scanner accounts for staff
- Print QR codes for backup

### Conferences
- Create multiple events for different sessions
- Use plus_ones for guest passes
- Export attendee lists from admin

### Private Parties
- Set low max_tickets limit
- Share event URL via invitation
- Monitor check-ins in real-time

### Webinars
- Use for attendance tracking
- Generate QR codes for certificates
- Track participant counts

## 💡 Pro Tips

1. **Test thoroughly** before the event
2. **Have backup scanners** ready
3. **Print some QR codes** as backup
4. **Train staff** on scanner usage
5. **Monitor capacity** in admin panel
6. **Keep admin credentials secure**
7. **Test camera access** beforehand
8. **Have WiFi backup plan** ready

## 📞 Support

### Documentation
- README.md - Full documentation
- DEPLOYMENT_GUIDE.md - Heroku deployment
- PROJECT_STRUCTURE.md - Code structure

### Resources
- Django Documentation: https://docs.djangoproject.com/
- Bootstrap Documentation: https://getbootstrap.com/docs/
- html5-qrcode: https://github.com/mebjas/html5-qrcode

### Common Issues
- Check logs: `python manage.py runserver` output
- Verify dependencies: `pip list`
- Test database: `python manage.py dbshell`

## ✅ Checklist

Before your event:
- [ ] Create event in admin panel
- [ ] Test ticket creation
- [ ] Test QR code generation
- [ ] Test QR code scanning
- [ ] Verify camera access works
- [ ] Create scanner accounts
- [ ] Train staff on scanner usage
- [ ] Test on mobile devices
- [ ] Verify capacity limits work
- [ ] Have backup plan ready

## 🎉 You're Ready!

Your QR Ticket System is now running. Enjoy using it for your events!

For questions or issues, refer to the full documentation in README.md and DEPLOYMENT_GUIDE.md.

