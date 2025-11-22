import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projectsite.settings')
django.setup()

from django.contrib.auth.models import User
from paymentorg.models import Officer

u = User.objects.get(username='superofficer')
print(f'✓ User: {u.username}')
print(f'✓ Has officer_profile: {hasattr(u, "officer_profile")}')

if hasattr(u, 'officer_profile'):
    print(f'✓ is_super_officer: {u.officer_profile.is_super_officer}')
    print(f'✓ Organization: {u.officer_profile.organization}')
else:
    print('✗ No officer_profile found!')
