from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from tickets.models import Event
from datetime import datetime, timedelta


class Command(BaseCommand):
    help = 'Initialize database with sample data and users'

    def handle(self, *args, **options):
        self.stdout.write('Initializing database...')
        
        # Create admin user if it doesn't exist
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            self.stdout.write(self.style.SUCCESS('✓ Created admin user (username: admin, password: admin123)'))
        else:
            self.stdout.write('✓ Admin user already exists')
        
        # Create scanner user if it doesn't exist
        if not User.objects.filter(username='scanner').exists():
            User.objects.create_user('scanner', 'scanner@example.com', 'scanner123')
            self.stdout.write(self.style.SUCCESS('✓ Created scanner user (username: scanner, password: scanner123)'))
        else:
            self.stdout.write('✓ Scanner user already exists')
        
        # Create sample event if it doesn't exist
        if not Event.objects.filter(name='Tech Conference 2025').exists():
            Event.objects.create(
                name='Tech Conference 2025',
                date_time=datetime.now() + timedelta(days=30),
                location='Istanbul Convention Center',
                max_tickets=100
            )
            self.stdout.write(self.style.SUCCESS('✓ Created sample event: Tech Conference 2025'))
        else:
            self.stdout.write('✓ Sample event already exists')
        
        self.stdout.write(self.style.SUCCESS('\n✅ Database initialization complete!'))
        self.stdout.write('\nYou can now:')
        self.stdout.write('  - Visit /event/1/ to create tickets')
        self.stdout.write('  - Login to /admin/ with username: admin, password: admin123')
        self.stdout.write('  - Login to /scanner/ with username: scanner, password: scanner123')
