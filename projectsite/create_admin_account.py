import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projectsite.settings')
django.setup()

from django.contrib.auth.models import User

# Create superuser account
username = 'admin2'
email = 'admin2@unipay.local'
password = 'Admin2@12345'

user, created = User.objects.get_or_create(
    username=username,
    defaults={
        'email': email,
        'is_staff': True,
        'is_superuser': True,
    }
)

if created:
    user.set_password(password)
    user.save()
    print(f"✅ Super Admin Account Created!")
    print(f"   Username: {username}")
    print(f"   Email: {email}")
    print(f"   Password: {password}")
else:
    user.set_password(password)
    user.save()
    print(f"✅ Super Admin Account Updated!")
    print(f"   Username: {username}")
    print(f"   Email: {email}")
    print(f"   Password: {password}")
