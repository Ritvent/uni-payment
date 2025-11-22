#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projectsite.settings')
django.setup()

from django.contrib.auth.models import User

# Set password for superstudent
user = User.objects.get(username='superstudent')
user.set_password('SuperStudent@123')
user.save()

print("✅ Password set for superstudent (Admin/Staff Account):")
print(f"Username: superstudent")
print(f"Password: SuperStudent@123")
print(f"\nYou can now:")
print(f"1. Login at: http://localhost:8080/login/")
print(f"2. Go to Promote Officer at: http://localhost:8080/staff/officers/promote/")
