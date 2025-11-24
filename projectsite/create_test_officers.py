"""
Create test officers for organization hierarchy testing
Tests the following scenarios:
1. College-level officer with promotion authority - can see all programs under college
2. Program-level officer - can see only their program
3. Program-level officer with promotion authority - can promote/demote in their program
4. Super admin - can see everything
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projectsite.settings')
django.setup()

from django.contrib.auth.models import User
from paymentorg.models import Officer, Student, Organization, UserProfile, College, Course, AcademicYearConfig
from decimal import Decimal

def create_college_and_programs():
    """Create College of Sciences with 3 programs"""
    # Create college
    college, _ = College.objects.get_or_create(
        name='College of Sciences',
        defaults={
            'code': 'COS',
            'description': 'College of Sciences with multiple programs'
        }
    )
    
    # Create programs under college
    programs = {
        'COMPUTER_SCIENCE': 'Computer Science',
        'ENVIRONMENTAL_SCIENCE': 'Environmental Science',
        'INFORMATION_TECHNOLOGY': 'Information Technology'
    }
    
    program_courses = {}
    for program_type, program_name in programs.items():
        course, _ = Course.objects.get_or_create(
            name=program_name,
            college=college,
            defaults={
                'code': program_type[:3].upper(),
                'program_type': program_type,
                'description': f'{program_name} program'
            }
        )
        program_courses[program_type] = course
    
    return college, program_courses

def create_test_officers():
    """Create test officers at different hierarchy levels"""
    
    college, program_courses = create_college_and_programs()
    
    # Get academic year for student creation
    academic_year = AcademicYearConfig.objects.filter(is_active=True).first()
    
    print("\n" + "="*70)
    print("CREATING ORGANIZATION HIERARCHY TEST ACCOUNTS")
    print("="*70)
    
    # 1. Create College-Level Officer (can see all programs in college)
    print("\n1️⃣  Creating COLLEGE-LEVEL OFFICER (can see all programs)")
    print("-" * 70)
    
    # Create or get college-level organization
    college_org, _ = Organization.objects.get_or_create(
        name='College of Sciences Administration',
        defaults={
            'code': 'COSA',
            'hierarchy_level': 'COLLEGE',
            'department': 'College of Sciences',
            'fee_tier': 'TIER_2',
            'contact_email': 'cos@unipay.local',
            'contact_phone': '555-0001',
            'booth_location': 'College Building'
        }
    )
    
    college_user, _ = User.objects.get_or_create(
        username='college_officer',
        defaults={
            'email': 'college_officer@unipay.local',
            'first_name': 'College',
            'last_name': 'Officer'
        }
    )
    college_user.set_password('CollegeOfficer@123')
    college_user.save()
    
    college_officer, _ = Officer.objects.get_or_create(
        user=college_user,
        defaults={
            'organization': college_org,
            'role': 'College Administrator',
            'can_process_payments': True,
            'can_void_payments': True,
            'can_generate_reports': True,
            'can_promote_officers': True,  # Can promote officers in their organization
            'is_super_officer': False
        }
    )
    
    UserProfile.objects.update_or_create(
        user=college_user,
        defaults={'is_officer': True}
    )
    
    print(f"✅ College-Level Officer Created")
    print(f"   Username: college_officer")
    print(f"   Password: CollegeOfficer@123")
    print(f"   Organization: {college_org.name}")
    print(f"   Role: {college_officer.role}")
    print(f"   Can Promote Officers: {college_officer.can_promote_officers}")
    print(f"   Access: Can see all programs under College of Sciences")
    
    # 2. Create Program-Level Officer (Computer Science)
    print("\n2️⃣  Creating PROGRAM-LEVEL OFFICER (Computer Science only)")
    print("-" * 70)
    
    # Create program-level organization for Computer Science
    cs_org, _ = Organization.objects.get_or_create(
        name='Computer Science Student Government',
        defaults={
            'code': 'CSSG',
            'hierarchy_level': 'PROGRAM',
            'parent_organization': college_org,
            'department': 'College of Sciences',
            'fee_tier': 'TIER_1',
            'program_affiliation': 'COMPUTER_SCIENCE',
            'contact_email': 'cssg@unipay.local',
            'contact_phone': '555-0002',
            'booth_location': 'CS Building Room 101'
        }
    )
    
    cs_user, _ = User.objects.get_or_create(
        username='cs_officer',
        defaults={
            'email': 'cs_officer@unipay.local',
            'first_name': 'CS',
            'last_name': 'Officer'
        }
    )
    cs_user.set_password('CSProgram@123')
    cs_user.save()
    
    cs_officer, _ = Officer.objects.get_or_create(
        user=cs_user,
        defaults={
            'organization': cs_org,
            'role': 'Treasurer',
            'can_process_payments': True,
            'can_void_payments': False,
            'can_generate_reports': False,
            'can_promote_officers': False,  # Cannot promote
            'is_super_officer': False
        }
    )
    
    UserProfile.objects.update_or_create(
        user=cs_user,
        defaults={'is_officer': True}
    )
    
    print(f"✅ Program-Level Officer Created")
    print(f"   Username: cs_officer")
    print(f"   Password: CSProgram@123")
    print(f"   Organization: {cs_org.name}")
    print(f"   Role: {cs_officer.role}")
    print(f"   Can Promote Officers: {cs_officer.can_promote_officers}")
    print(f"   Access: Can see ONLY Computer Science program")
    
    # 3. Create Program-Level Officer with Promotion Authority (Environmental Science)
    print("\n3️⃣  Creating PROGRAM-LEVEL OFFICER WITH PROMOTION (Environmental Science)")
    print("-" * 70)
    
    # Create program-level organization for Environmental Science
    es_org, _ = Organization.objects.get_or_create(
        name='Environmental Science Club',
        defaults={
            'code': 'ESCLUB',
            'hierarchy_level': 'PROGRAM',
            'parent_organization': college_org,
            'department': 'College of Sciences',
            'fee_tier': 'TIER_1',
            'program_affiliation': 'ENVIRONMENTAL_SCIENCE',
            'contact_email': 'esclub@unipay.local',
            'contact_phone': '555-0003',
            'booth_location': 'Science Hall Ground Floor'
        }
    )
    
    es_user, _ = User.objects.get_or_create(
        username='es_officer',
        defaults={
            'email': 'es_officer@unipay.local',
            'first_name': 'EnvSci',
            'last_name': 'Officer'
        }
    )
    es_user.set_password('EnvScience@123')
    es_user.save()
    
    es_officer, _ = Officer.objects.get_or_create(
        user=es_user,
        defaults={
            'organization': es_org,
            'role': 'President',
            'can_process_payments': True,
            'can_void_payments': True,
            'can_generate_reports': False,
            'can_promote_officers': True,  # CAN promote in their program
            'is_super_officer': False
        }
    )
    
    UserProfile.objects.update_or_create(
        user=es_user,
        defaults={'is_officer': True}
    )
    
    print(f"✅ Program-Level Officer with Promotion Authority Created")
    print(f"   Username: es_officer")
    print(f"   Password: EnvScience@123")
    print(f"   Organization: {es_org.name}")
    print(f"   Role: {es_officer.role}")
    print(f"   Can Promote Officers: {es_officer.can_promote_officers}")
    print(f"   Access: Can see ONLY Environmental Science program + promote officers")
    
    # 4. Super Admin (created in previous steps, just show details)
    print("\n4️⃣  SUPER ADMIN (Full Access)")
    print("-" * 70)
    print(f"✅ Super Admin Credentials")
    print(f"   Username: admin2")
    print(f"   Password: Admin2@12345")
    print(f"   Access: All organizations, all data, all functions")
    
    print("\n" + "="*70)
    print("TEST SCENARIOS")
    print("="*70)
    
    scenarios = """
    
    🎯 TESTING SCENARIOS:
    
    1. COLLEGE-LEVEL OFFICER (college_officer / CollegeOfficer@123)
       ✓ Login and go to Officer Dashboard
       ✓ Should see ALL programs under College of Sciences
       ✓ Click "Promote Officer" - should see students from all 3 programs
       ✓ Should be able to assign officers to any program in the college
       ✓ Can access admin pages for entire college hierarchy
       
    2. PROGRAM-LEVEL OFFICER - NO PROMOTION (cs_officer / CSProgram@123)
       ✓ Login and go to Officer Dashboard
       ✓ Should see ONLY Computer Science program data
       ✓ Should NOT see "Promote Officer" button (no can_promote_officers)
       ✓ Cannot access other programs' data
       ✓ Can process payments only
       
    3. PROGRAM-LEVEL OFFICER - WITH PROMOTION (es_officer / EnvScience@123)
       ✓ Login and go to Officer Dashboard
       ✓ Should see ONLY Environmental Science program data
       ✓ Should see "Promote Officer" and "Demote Officer" buttons
       ✓ Can promote/demote officers in Environmental Science program only
       ✓ Cannot promote officers outside their program
       
    4. SUPER ADMIN (admin2 / Admin2@12345)
       ✓ Login with /admin/ path
       ✓ Can see all organizations and students
       ✓ Can use Django admin interface
       ✓ Can access all staff pages directly
       
    🔒 SECURITY TESTS:
    
    ✓ Try accessing /staff/students/ as cs_officer - should see only CS students
    ✓ Try accessing /staff/students/ as es_officer - should see only EnvSci students
    ✓ Try accessing /staff/students/ as college_officer - should see all under college
    ✓ Try accessing students from different program as cs_officer - should be denied
    """
    
    print(scenarios)
    
    print("="*70)
    print("ORGANIZATION HIERARCHY")
    print("="*70)
    print("""
    College of Sciences (COLLEGE LEVEL - college_officer)
    ├── Computer Science (PROGRAM LEVEL - cs_officer)
    ├── Environmental Science (PROGRAM LEVEL - es_officer)
    └── Information Technology (PROGRAM LEVEL - [no officer yet])
    """)
    
    print("="*70 + "\n")

if __name__ == '__main__':
    create_test_officers()
