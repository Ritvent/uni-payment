#!/bin/bash

# Create Environmental Science and Compendium Officers
# Run this in PythonAnywhere bash console

cd /home/dian1612/uni-payment/projectsite

python manage.py shell << 'PYEOF'
from django.contrib.auth.models import User
from paymentorg.models import Officer, Organization, UserProfile

print("\n" + "="*80)
print("CREATING ENVIRONMENTAL SCIENCE OFFICER")
print("="*80)

# Get parent organization
try:
    parent = Organization.objects.get(code='ALLORG')
    print(f"✓ Found parent organization: {parent.name}")
except Organization.DoesNotExist:
    print("ERROR: Parent organization 'ALLORG' not found!")
    print("Please run 'python manage.py create_promotion_officers' first")
    exit(1)

# Create Environmental Science organization
org_env, created = Organization.objects.get_or_create(
    code='ENVSCIENCE',
    defaults={
        'name': 'Environmental Science',
        'hierarchy_level': 'PROGRAM',
        'parent_organization': parent,
        'department': 'Promotion Authority',
        'fee_tier': 'TIER_1',
        'program_affiliation': 'ENVIRONMENTAL_SCIENCE',
        'contact_email': 'envscience@unipay.local',
        'contact_phone': '555-0000',
        'booth_location': 'Environmental Science Office'
    }
)
print(f"✓ Organization: {org_env.name}")

# Create user
user_env, _ = User.objects.get_or_create(
    username='envscience_officer',
    defaults={
        'email': 'envscience_officer@unipay.local',
        'first_name': 'EnvScience',
        'last_name': 'Officer'
    }
)
user_env.set_password('EnvScience@123')
user_env.save()
print(f"✓ User: {user_env.username}")

# Create officer
officer_env, _ = Officer.objects.get_or_create(
    user=user_env,
    defaults={
        'employee_id': 'ENVSCIENCE_001',
        'first_name': 'EnvScience',
        'last_name': 'Officer',
        'email': 'envscience_officer@unipay.local',
        'phone_number': '555-0000',
        'organization': org_env,
        'role': 'Program Head',
        'can_process_payments': True,
        'can_void_payments': True,
        'can_generate_reports': True,
        'can_promote_officers': True,
        'is_super_officer': False
    }
)
if not _:
    officer_env.can_promote_officers = True
    officer_env.organization = org_env
    officer_env.save()
print(f"✓ Officer: {officer_env.employee_id}")

# Create user profile
UserProfile.objects.update_or_create(
    user=user_env,
    defaults={'is_officer': True}
)
print(f"✓ User Profile: is_officer=True")

print("\n" + "="*80)
print("CREATING COMPENDIUM OFFICER")
print("="*80)

# Create Compendium organization (college-level publication under ALLORG)
org_comp, created = Organization.objects.get_or_create(
    code='COMPENDIUM',
    defaults={
        'name': 'Compendium',
        'hierarchy_level': 'COLLEGE',
        'parent_organization': parent,
        'department': 'Promotion Authority',
        'fee_tier': 'TIER_1',
        'program_affiliation': 'COMPENDIUM',
        'contact_email': 'compendium@unipay.local',
        'contact_phone': '555-0000',
        'booth_location': 'Compendium Office'
    }
)
print(f"✓ Organization: {org_comp.name}")
print(f"✓ Parent Organization: {parent.name}")

# Create user
user_comp, _ = User.objects.get_or_create(
    username='compendium_officer',
    defaults={
        'email': 'compendium_officer@unipay.local',
        'first_name': 'Compendium',
        'last_name': 'Officer'
    }
)
user_comp.set_password('Compendium@123')
user_comp.save()
print(f"✓ User: {user_comp.username}")

# Create officer
officer_comp, _ = Officer.objects.get_or_create(
    user=user_comp,
    defaults={
        'employee_id': 'COMPENDIUM_001',
        'first_name': 'Compendium',
        'last_name': 'Officer',
        'email': 'compendium_officer@unipay.local',
        'phone_number': '555-0000',
        'organization': org_comp,
        'role': 'College Publication Editor',
        'can_process_payments': True,
        'can_void_payments': True,
        'can_generate_reports': True,
        'can_promote_officers': True,
        'is_super_officer': False
    }
)
if not _:
    officer_comp.can_promote_officers = True
    officer_comp.organization = org_comp
    officer_comp.save()
print(f"✓ Officer: {officer_comp.employee_id}")

# Create user profile
UserProfile.objects.update_or_create(
    user=user_comp,
    defaults={'is_officer': True}
)
print(f"✓ User Profile: is_officer=True")

print("\n" + "="*80)
print("✅ ACCOUNTS CREATED SUCCESSFULLY")
print("="*80)
print("\nEnvironmental Science Officer:")
print(f"  Username: envscience_officer")
print(f"  Password: EnvScience@123")
print(f"  Promotion Authority: YES")

print("\nCompendium Officer:")
print(f"  Username: compendium_officer")
print(f"  Password: Compendium@123")
print(f"  Promotion Authority: YES")
print("\n")

PYEOF
