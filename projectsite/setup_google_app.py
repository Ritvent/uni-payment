import os
import django
import sys

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projectsite.settings')
django.setup()

from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp

def setup_google_app():
    print("Setting up Google Social Application...")
    
    # 1. Ensure the Site exists (SITE_ID = 2 based on your settings)
    site_id = 2
    try:
        site = Site.objects.get(id=site_id)
        print(f"Found Site ID {site_id}: {site.domain}")
    except Site.DoesNotExist:
        # If ID 2 doesn't exist, try to find any site or create one
        print(f"Site ID {site_id} not found. Checking for existing sites...")
        site = Site.objects.first()
        if site:
            print(f"Using existing site: {site.domain} (ID: {site.id})")
            # Update settings.py SITE_ID might be needed if this mismatches, 
            # but for now we just link the app to this site.
        else:
            print("No sites found. Creating default site...")
            site = Site.objects.create(domain='127.0.0.1:8000', name='UniPay Local')
            print(f"Created site: {site.domain} (ID: {site.id})")

    # 2. Create or Update the Google SocialApp
    # NOTE: You will need to update these values in the Admin Panel later!
    client_id = "YOUR_GOOGLE_CLIENT_ID_HERE" 
    secret = "YOUR_GOOGLE_CLIENT_SECRET_HERE"
    
    app, created = SocialApp.objects.get_or_create(
        provider='google',
        defaults={
            'name': 'Google',
            'client_id': client_id,
            'secret': secret,
        }
    )
    
    if created:
        print("Created new Google SocialApp.")
    else:
        print("Found existing Google SocialApp.")
    
    # 3. Link the App to the Site
    app.sites.add(site)
    print(f"Linked Google App to site: {site.domain}")
    
    print("\nSUCCESS! The login page should now render.")
    print("IMPORTANT: Log in to /admin/ to update the Client ID and Secret with your real keys.")

if __name__ == '__main__':
    setup_google_app()
