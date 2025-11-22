"""
Create test officers with PROMOTION AUTHORITY for all organizations
Each officer can promote/demote other officers within their organization
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projectsite.settings')
django.setup()

from django.contrib.auth.models import User
from paymentorg.models import Officer, Organization, UserProfile

def create_promotion_authority_officers():
    """Create officers with promotion authority for: ALL, MedBio, MarineBio, IT, ComSci"""
    
    print("\n" + "="*80)
    print("CREATING OFFICERS WITH PROMOTION AUTHORITY FOR ALL ORGANIZATIONS")
    print("="*80)
    
    # Define organizations and their officer credentials
    organizations_config = [
        {
            'org_name': 'ALL Organizations Admin',
            'org_code': 'ALLORG',
            'org_level': 'COLLEGE',
            'username': 'all_org_officer',
            'password': 'AllOrg@123',
            'first_name': 'All',
            'last_name': 'Organizations',
            'employee_id': 'ALL_001',
            'role': 'College Administrator',
            'description': 'Can promote/demote in ALL organizations',
            'program_affiliation': 'ALL'
        },
        {
            'org_name': 'Medical Biology',
            'org_code': 'MEDBIO',
            'org_level': 'PROGRAM',
            'parent_org_code': 'ALLORG',
            'username': 'medbio_officer',
            'password': 'MedBio@123',
            'first_name': 'MedBio',
            'last_name': 'Officer',
            'employee_id': 'MEDBIO_001',
            'role': 'Program Head',
            'description': 'Can promote/demote in Medical Biology only',
            'program_affiliation': 'MEDICAL_BIOLOGY'
        },
        {
            'org_name': 'Marine Biology',
            'org_code': 'MARINEBIO',
            'org_level': 'PROGRAM',
            'parent_org_code': 'ALLORG',
            'username': 'marinebio_officer',
            'password': 'MarineBio@123',
            'first_name': 'MarineBio',
            'last_name': 'Officer',
            'employee_id': 'MARINEBIO_001',
            'role': 'Program Head',
            'description': 'Can promote/demote in Marine Biology only',
            'program_affiliation': 'MARINE_BIOLOGY'
        },
        {
            'org_name': 'Information Technology',
            'org_code': 'IT',
            'org_level': 'PROGRAM',
            'parent_org_code': 'ALLORG',
            'username': 'it_officer',
            'password': 'IT@123',
            'first_name': 'IT',
            'last_name': 'Officer',
            'employee_id': 'IT_001',
            'role': 'Program Head',
            'description': 'Can promote/demote in Information Technology only',
            'program_affiliation': 'INFORMATION_TECHNOLOGY'
        },
        {
            'org_name': 'Computer Science',
            'org_code': 'COMSCI',
            'org_level': 'PROGRAM',
            'parent_org_code': 'ALLORG',
            'username': 'comsci_officer',
            'password': 'ComSci@123',
            'first_name': 'ComSci',
            'last_name': 'Officer',
            'employee_id': 'COMSCI_001',
            'role': 'Program Head',
            'description': 'Can promote/demote in Computer Science only',
            'program_affiliation': 'COMPUTER_SCIENCE'
        },
        {
            'org_name': 'Environmental Science',
            'org_code': 'ENVSCIENCE',
            'org_level': 'PROGRAM',
            'parent_org_code': 'ALLORG',
            'username': 'envscience_officer',
            'password': 'EnvScience@123',
            'first_name': 'EnvScience',
            'last_name': 'Officer',
            'employee_id': 'ENVSCIENCE_001',
            'role': 'Program Head',
            'description': 'Can promote/demote in Environmental Science only',
            'program_affiliation': 'ENVIRONMENTAL_SCIENCE'
        },
        {
            'org_name': 'Compendium',
            'org_code': 'COMPENDIUM',
            'org_level': 'COLLEGE',
            'username': 'compendium_officer',
            'password': 'Compendium@123',
            'first_name': 'Compendium',
            'last_name': 'Officer',
            'employee_id': 'COMPENDIUM_001',
            'role': 'College Publication Editor',
            'description': 'Can promote/demote in Compendium (college publication)',
            'program_affiliation': 'COMPENDIUM'
        }
    ]
    
    parent_org = None
    accounts = []
    
    for config in organizations_config:
        print(f"\n{'='*80}")
        print(f"Creating: {config['org_name']}")
        print(f"{'='*80}")
        
        # Get or create parent organization first
        if config['org_level'] == 'COLLEGE':
            org, created = Organization.objects.get_or_create(
                code=config['org_code'],
                defaults={
                    'name': config['org_name'],
                    'hierarchy_level': config['org_level'],
                    'department': 'Promotion Authority',
                    'fee_tier': 'TIER_1',
                    'program_affiliation': config['program_affiliation'],
                    'contact_email': f"{config['org_code'].lower()}@unipay.local",
                    'contact_phone': '555-0000',
                    'booth_location': 'Main Office'
                }
            )
            parent_org = org
            print(f"✓ Organization created: {org.name}")
        else:
            # Get parent organization
            try:
                parent = Organization.objects.get(code=config.get('parent_org_code'))
            except Organization.DoesNotExist:
                print(f"ERROR: Parent organization {config.get('parent_org_code')} not found!")
                continue
            
            org, created = Organization.objects.get_or_create(
                code=config['org_code'],
                defaults={
                    'name': config['org_name'],
                    'hierarchy_level': config['org_level'],
                    'parent_organization': parent,
                    'department': 'Promotion Authority',
                    'fee_tier': 'TIER_1',
                    'program_affiliation': config['program_affiliation'],
                    'contact_email': f"{config['org_code'].lower()}@unipay.local",
                    'contact_phone': '555-0000',
                    'booth_location': f'{config["org_name"]} Office'
                }
            )
            print(f"✓ Organization created: {org.name}")
            print(f"  Parent: {parent.name}")
        
        # Create or update user
        user, user_created = User.objects.get_or_create(
            username=config['username'],
            defaults={
                'email': f"{config['username']}@unipay.local",
                'first_name': config['first_name'],
                'last_name': config['last_name']
            }
        )
        user.set_password(config['password'])
        user.save()
        print(f"✓ User created/updated: {user.username}")
        
        # Create or update officer
        officer, officer_created = Officer.objects.get_or_create(
            user=user,
            defaults={
                'employee_id': config['employee_id'],
                'first_name': config['first_name'],
                'last_name': config['last_name'],
                'email': f"{config['username']}@unipay.local",
                'phone_number': '555-0000',
                'organization': org,
                'role': config['role'],
                'can_process_payments': True,
                'can_void_payments': True,
                'can_generate_reports': True,
                'can_promote_officers': True,  # ✅ PROMOTION AUTHORITY
                'is_super_officer': False
            }
        )
        
        # Update if already exists (to ensure promotion authority is set)
        if not officer_created:
            officer.can_promote_officers = True
            officer.organization = org
            officer.save()
            print(f"✓ Officer updated: {officer.employee_id}")
        else:
            print(f"✓ Officer created: {officer.employee_id}")
        
        # Create user profile
        UserProfile.objects.update_or_create(
            user=user,
            defaults={'is_officer': True}
        )
        
        # Store account info for display
        accounts.append({
            'org_name': config['org_name'],
            'username': config['username'],
            'password': config['password'],
            'role': config['role'],
            'description': config['description'],
            'org_code': config['org_code']
        })
        
        print(f"✓ Permissions: Can promote/demote officers")
        print(f"✓ Access: {config['description']}")
    
    # Display all created accounts
    print("\n\n" + "="*80)
    print("PROMOTION AUTHORITY ACCOUNTS CREATED")
    print("="*80)
    
    for i, account in enumerate(accounts, 1):
        print(f"\n{i}. {account['org_name']}")
        print(f"   {'─' * 76}")
        print(f"   Username: {account['username']}")
        print(f"   Password: {account['password']}")
        print(f"   Role: {account['role']}")
        print(f"   Promotion Authority: ✅ YES")
        print(f"   Access: {account['description']}")
    
    # Display testing instructions
    print("\n\n" + "="*80)
    print("TESTING INSTRUCTIONS")
    print("="*80)
    
    instructions = """
    
    🔐 LOGIN & ACCESS CONTROL:
    
    ✓ Use any of the credentials above to login
    ✓ Each officer will see ONLY their organization's data
    ✓ ALL organization officer (all_org_officer) will see ALL organizations
    ✓ Promotion buttons will be visible for all officers
    
    📋 TESTING SCENARIOS:
    
    1. Test College-Level Access:
       - Login as: all_org_officer (AllOrg@123)
       - Should see: All organizations and all students
       - Can promote: Officers from any organization
       
    2. Test Program-Level Access - Medical Biology:
       - Login as: medbio_officer (MedBio@123)
       - Should see: Only Medical Biology students/officers
       - Can promote: Only within Medical Biology
       
    3. Test Program-Level Access - Marine Biology:
       - Login as: marinebio_officer (MarineBio@123)
       - Should see: Only Marine Biology students/officers
       - Can promote: Only within Marine Biology
       
    4. Test Program-Level Access - Information Technology:
       - Login as: it_officer (IT@123)
       - Should see: Only IT students/officers
       - Can promote: Only within Information Technology
       
    5. Test Program-Level Access - Computer Science:
       - Login as: comsci_officer (ComSci@123)
       - Should see: Only Computer Science students/officers
       - Can promote: Only within Computer Science
    
    6. Test Program-Level Access - Environmental Science:
       - Login as: envscience_officer (EnvScience@123)
       - Should see: Only Environmental Science students/officers
       - Can promote: Only within Environmental Science
    
    7. Test College-Level Access - Compendium:
       - Login as: compendium_officer (Compendium@123)
       - Should see: Only Compendium students/officers
       - Can promote: Only within Compendium
    
    🔒 SECURITY VERIFICATION:
    
    ✓ Try accessing other program's data as program officer → Should be denied
    ✓ Try accessing /staff/students/ → Should show only accessible students
    ✓ Try promoting student from different program → Should be denied
    ✓ Check database: All officers have can_promote_officers = TRUE
    ✓ Verify: Officers can see/access their organization only (except all_org_officer)
    
    📊 DATA FILTERING:
    
    ✓ medbio_officer sees: Medical Biology students & officers only
    ✓ marinebio_officer sees: Marine Biology students & officers only
    ✓ it_officer sees: IT students & officers only
    ✓ comsci_officer sees: Computer Science students & officers only
    ✓ all_org_officer sees: ALL students & officers
    
    ✨ FEATURE VERIFICATION:
    
    ✓ "Promote Officer" button visible: YES (all have promotion authority)
    ✓ "Demote Officer" button visible: YES (all have promotion authority)
    ✓ Can promote students to officers: YES (within accessible orgs)
    ✓ Can demote officers to students: YES (within accessible orgs)
    ✓ Can assign can_promote_officers permission: ADMIN ONLY
    """
    
    print(instructions)
    
    # Display organization hierarchy
    print("\n" + "="*80)
    print("ORGANIZATION HIERARCHY")
    print("="*80)
    print("""
    ALL Organizations (COLLEGE LEVEL)
    ├── Medical Biology (PROGRAM LEVEL)
    ├── Marine Biology (PROGRAM LEVEL)
    ├── Information Technology (PROGRAM LEVEL)
    ├── Computer Science (PROGRAM LEVEL)
    └── Environmental Science (PROGRAM LEVEL)
    
    Compendium (COLLEGE LEVEL - College Publication)
    
    All officers at program level have access to their program only.
    All organization admin (all_org_officer) has access to all organizations.
    Compendium officer has access to Compendium only.
    """)
    
    print("="*80 + "\n")

if __name__ == '__main__':
    create_promotion_authority_officers()
