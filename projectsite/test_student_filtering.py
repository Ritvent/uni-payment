"""
Test script to verify student filtering in promotion form
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projectsite.settings')
django.setup()

from django.contrib.auth.models import User
from paymentorg.models import Officer, Student, Organization, Course

print("\n" + "="*80)
print("TESTING STUDENT FILTERING FOR PROMOTION FORM")
print("="*80)

# Test 1: Check available organizations
print("\n1. Available Organizations:")
print("-" * 80)
orgs = Organization.objects.all()
for org in orgs:
    print(f"  • {org.name} ({org.code})")
    print(f"    Level: {org.hierarchy_level}, Program: {org.program_affiliation}")
    if org.parent_organization:
        print(f"    Parent: {org.parent_organization.name}")
    print()

# Test 2: Check available students
print("\n2. Available Students:")
print("-" * 80)
students = Student.objects.filter(is_active=True)
print(f"Total active students: {students.count()}")
for student in students[:5]:  # Show first 5
    print(f"  • {student.first_name} {student.last_name} (ID: {student.student_id_number})")
    if student.course:
        print(f"    Course: {student.course.name} ({student.course.program_type})")
    print()

# Test 3: Check officers and their accessible students
print("\n3. Testing Officer Access:")
print("-" * 80)
officers = Officer.objects.filter(is_active=True)
for officer in officers[:3]:  # Test first 3 officers
    print(f"\nOfficer: {officer.get_full_name()}")
    print(f"Organization: {officer.organization.name} ({officer.organization.program_affiliation})")
    print(f"Can Promote: {officer.can_promote_officers}")
    
    # Get accessible organizations
    accessible_orgs = officer.organization.get_accessible_organizations()
    print(f"Accessible Organizations: {[org.name for org in accessible_orgs]}")
    
    # Build query to match the view logic
    from django.db.models import Q
    students_query = Student.objects.filter(is_active=True)
    q_filter = Q()
    
    for org in accessible_orgs:
        if org.program_affiliation == 'ALL':
            # College-level org
            if org.parent_organization:
                q_filter |= Q(course__college=org.parent_organization.id)
        else:
            # Program-specific org
            program_type = org.program_affiliation
            q_filter |= Q(course__program_type=program_type)
    
    if q_filter:
        accessible_students = students_query.filter(q_filter).distinct()
    else:
        accessible_students = Student.objects.none()
    
    print(f"Accessible Students: {accessible_students.count()}")
    for student in accessible_students[:3]:  # Show first 3
        print(f"  - {student.first_name} {student.last_name} ({student.course.program_type if student.course else 'N/A'})")

print("\n" + "="*80)
print("TEST COMPLETE")
print("="*80 + "\n")
