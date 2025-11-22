"""
Update existing promotion authority organizations with correct program affiliations
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projectsite.settings')
django.setup()

from paymentorg.models import Organization

print("\n" + "="*80)
print("UPDATING ORGANIZATION PROGRAM AFFILIATIONS")
print("="*80)

# Update Medical Biology
try:
    medbio = Organization.objects.get(code='MEDBIO')
    medbio.program_affiliation = 'MEDICAL_BIOLOGY'
    medbio.save()
    print(f"\n✓ Updated {medbio.name}: program_affiliation = MEDICAL_BIOLOGY")
except Organization.DoesNotExist:
    print("\n✗ Medical Biology organization not found")

# Update Marine Biology
try:
    marinebio = Organization.objects.get(code='MARINEBIO')
    marinebio.program_affiliation = 'MARINE_BIOLOGY'
    marinebio.save()
    print(f"✓ Updated {marinebio.name}: program_affiliation = MARINE_BIOLOGY")
except Organization.DoesNotExist:
    print("✗ Marine Biology organization not found")

# Update Information Technology
try:
    it = Organization.objects.get(code='IT')
    it.program_affiliation = 'INFORMATION_TECHNOLOGY'
    it.save()
    print(f"✓ Updated {it.name}: program_affiliation = INFORMATION_TECHNOLOGY")
except Organization.DoesNotExist:
    print("✗ Information Technology organization not found")

# Update Computer Science
try:
    comsci = Organization.objects.get(code='COMSCI')
    comsci.program_affiliation = 'COMPUTER_SCIENCE'
    comsci.save()
    print(f"✓ Updated {comsci.name}: program_affiliation = COMPUTER_SCIENCE")
except Organization.DoesNotExist:
    print("✗ Computer Science organization not found")

print("\n" + "="*80)
print("VERIFICATION")
print("="*80)

allorg = Organization.objects.get(code='ALLORG')
print(f"\nALL Organizations Admin:")
print(f"  Program Affiliation: {allorg.program_affiliation}")
print(f"  Child Organizations:")

for child in allorg.child_organizations.all():
    print(f"    • {child.name} ({child.code}): {child.program_affiliation}")

print("\n" + "="*80 + "\n")
