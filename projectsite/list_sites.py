import os
import sys
import django

# Add the project directory to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projectsite.settings')
django.setup()

from django.contrib.sites.models import Site
print("--- Sites ---")
for s in Site.objects.all():
    print(f"ID: {s.id}, Domain: {s.domain}, Name: {s.name}")
print("-------------")
