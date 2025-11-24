import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projectsite.settings')

def main():
    try:
        django.setup()
        from paymentorg.models import Officer, UserProfile
        from django.contrib.auth.models import User
        from django.db import transaction

        fixed = 0
        with transaction.atomic():
            for off in Officer.objects.select_related('user').all():
                UserProfile.objects.update_or_create(user=off.user, defaults={'is_officer': True})
                fixed += 1

        try:
            u = User.objects.get(username='dianara_kristy')
            target_state = getattr(getattr(u, 'user_profile', None), 'is_officer', None)
        except User.DoesNotExist:
            target_state = 'user not found'

        print(f"Synced {fixed} officer profiles; target user is_officer = {target_state}", flush=True)
    except Exception as e:
        print('ERROR during officer sync:', e, file=sys.stderr, flush=True)
        raise

if __name__ == '__main__':
    main()
