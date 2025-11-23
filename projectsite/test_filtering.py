#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projectsite.settings')
django.setup()

from paymentorg.models import Student, Officer, Organization, Course

# Find a program-level officer
officer = Officer.objects.filter(organization__hierarchy_level='PROGRAM', is_active=True).first()

if officer:
    print(f"\n=== Testing with Officer: {officer.user.username} ===")
    print(f"Organization: {officer.organization.name}")
    print(f"Hierarchy Level: {officer.organization.hierarchy_level}")
    print(f"Program Affiliation: {officer.organization.program_affiliation}")
    
    # Test the filtering logic
    org = officer.organization
    students_qs = Student.objects.filter(is_active=True).exclude(user__officer_profile__isnull=False).select_related('course')
    
    print(f"\nTotal active non-promoted students: {students_qs.count()}")
    
    if org.hierarchy_level == 'PROGRAM':
        if org.program_affiliation and org.program_affiliation != 'ALL':
            filtered = students_qs.filter(course__program_type=org.program_affiliation)
            print(f"Students with program_type = {org.program_affiliation}: {filtered.count()}")
            print("\nFiltered students:")
            for s in filtered[:5]:
                print(f"  - {s.first_name} {s.last_name} (Course: {s.course.name if s.course else 'None'} - {s.course.program_type if s.course else 'None'})")
        else:
            print(f"Organization has ALL affiliation - showing all students")
            print(f"Total: {students_qs.count()}")
    else:
        print(f"Not a PROGRAM level org")
else:
    print("No program-level officers found")
