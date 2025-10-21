# Deployment Guide for QR Ticket System

## Quick Start - Local Testing

The system is already set up and ready to test locally!

### Default Credentials

**Admin User:**
- Username: `admin`
- Password: `admin123`
- Access: http://localhost:8000/admin/

**Scanner User:**
- Username: `scanner`
- Password: `scanner123`
- Access: http://localhost:8000/login/

### Start the Development Server

```bash
cd /home/ubuntu/qr_ticket_system_project
python3 manage.py runserver
```

Then access:
- Event landing page: http://localhost:8000/event/1/
- Admin panel: http://localhost:8000/admin/
- Scanner dashboard: http://localhost:8000/scanner/ (requires login)

## Heroku Deployment Guide

### Step 1: Prerequisites

Install the Heroku CLI:
```bash
# On Ubuntu/Debian
curl https://cli-assets.heroku.com/install.sh | sh

# On macOS
brew tap heroku/brew && brew install heroku

# On Windows
# Download from: https://devcenter.heroku.com/articles/heroku-cli
```

### Step 2: Login to Heroku

```bash
heroku login
```

### Step 3: Initialize Git Repository

```bash
cd /home/ubuntu/qr_ticket_system_project
git init
git add .
git commit -m "Initial commit - QR Ticket System"
```

### Step 4: Create Heroku App

```bash
# Create a new Heroku app (replace 'your-app-name' with your desired name)
heroku create your-app-name

# Or let Heroku generate a random name
heroku create
```

### Step 5: Configure Environment Variables

```bash
# Generate a secure secret key
python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Set the secret key (replace with the generated key)
heroku config:set SECRET_KEY='your-generated-secret-key-here'

# Set debug to False for production
heroku config:set DEBUG=False
```

### Step 6: Add PostgreSQL Database

```bash
# Add PostgreSQL addon (free tier)
heroku addons:create heroku-postgresql:essential-0

# Verify database was added
heroku config:get DATABASE_URL
```

### Step 7: Deploy to Heroku

```bash
# Push code to Heroku
git push heroku main

# Or if your branch is named 'master'
git push heroku master
```

### Step 8: Run Database Migrations

```bash
# Run migrations on Heroku
heroku run python manage.py migrate

# Collect static files
heroku run python manage.py collectstatic --noinput
```

### Step 9: Create Admin and Scanner Users

```bash
# Create superuser
heroku run python manage.py createsuperuser

# Create scanner user via shell
heroku run python manage.py shell
```

In the shell, run:
```python
from django.contrib.auth.models import User
User.objects.create_user('scanner', 'scanner@example.com', 'your-secure-password')
exit()
```

### Step 10: Create Sample Event (Optional)

```bash
heroku run python manage.py shell
```

In the shell, run:
```python
from tickets.models import Event
from django.utils import timezone
from datetime import timedelta

Event.objects.create(
    name='Your Event Name',
    date_time=timezone.now() + timedelta(days=30),
    location='Your Event Location',
    max_tickets=100
)
exit()
```

### Step 11: Open Your App

```bash
heroku open
```

## Important Notes for Production

### 1. Media Files on Heroku

Heroku uses an ephemeral filesystem, meaning uploaded files (QR codes) will be deleted when the dyno restarts. For production, you should:

**Option A: Use AWS S3 (Recommended)**

Install django-storages:
```bash
pip install django-storages boto3
```

Add to `requirements.txt`:
```
django-storages==1.14.2
boto3==1.34.0
```

Update `settings.py`:
```python
# Add to INSTALLED_APPS
INSTALLED_APPS = [
    # ...
    'storages',
]

# S3 Configuration
if not DEBUG:
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_REGION_NAME = 'us-east-1'  # Change to your region
    AWS_S3_FILE_OVERWRITE = False
    AWS_DEFAULT_ACL = 'public-read'
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
```

Set environment variables:
```bash
heroku config:set AWS_ACCESS_KEY_ID='your-key'
heroku config:set AWS_SECRET_ACCESS_KEY='your-secret'
heroku config:set AWS_STORAGE_BUCKET_NAME='your-bucket-name'
```

**Option B: Regenerate QR Codes on Demand**

Modify the view to generate QR codes dynamically instead of storing them.

### 2. Security Checklist

- ✅ Change SECRET_KEY in production
- ✅ Set DEBUG=False
- ✅ Use strong passwords for admin and scanner users
- ✅ Enable HTTPS (automatic on Heroku)
- ✅ Configure ALLOWED_HOSTS if needed
- ✅ Set up regular database backups

### 3. Custom Domain (Optional)

```bash
# Add custom domain
heroku domains:add www.yourdomain.com

# Update ALLOWED_HOSTS in settings.py
ALLOWED_HOSTS = ['your-app-name.herokuapp.com', 'www.yourdomain.com']
```

### 4. Monitoring and Logs

```bash
# View logs
heroku logs --tail

# Check dyno status
heroku ps

# Restart dynos
heroku restart
```

### 5. Database Backups

```bash
# Create manual backup
heroku pg:backups:capture

# Download backup
heroku pg:backups:download

# Schedule automatic backups (requires paid plan)
heroku pg:backups:schedule DATABASE_URL --at '02:00 America/Los_Angeles'
```

## Troubleshooting

### Issue: Application Error (H10)

**Solution:** Check logs with `heroku logs --tail` and ensure:
- Procfile is correctly configured
- Dependencies are installed
- Database migrations are run

### Issue: Static Files Not Loading

**Solution:**
```bash
heroku run python manage.py collectstatic --noinput
```

### Issue: Database Connection Error

**Solution:** Verify DATABASE_URL is set:
```bash
heroku config:get DATABASE_URL
```

### Issue: QR Codes Not Displaying

**Solution:** 
- For development: Ensure media files are being served
- For production: Set up S3 storage (see above)

## Scaling

### Upgrade Dyno Type

```bash
# Upgrade to hobby dyno ($7/month)
heroku ps:scale web=1:hobby

# Upgrade to standard dyno ($25/month)
heroku ps:scale web=1:standard-1x
```

### Upgrade Database

```bash
# Upgrade to larger database plan
heroku addons:upgrade heroku-postgresql:standard-0
```

## Cost Estimate

**Free Tier:**
- Web dyno: Free (sleeps after 30 min of inactivity)
- PostgreSQL: Free (10,000 rows limit)
- Total: $0/month

**Production Tier:**
- Hobby dyno: $7/month
- Standard-0 PostgreSQL: $50/month
- Total: $57/month

## Support

For Heroku-specific issues:
- Documentation: https://devcenter.heroku.com/
- Status: https://status.heroku.com/

For Django issues:
- Documentation: https://docs.djangoproject.com/

