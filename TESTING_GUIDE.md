# UniPay Organization Hierarchy Testing Guide

## Quick Start - Test Credentials

### 🏢 College-Level Officer (Manages ALL programs)
```
Username: college_officer
Password: CollegeOfficer@123
Organization: College of Sciences Administration
Role: College Administrator
Permissions: Can promote officers
Access: ALL programs (CS, ES, IT) + All student/officer data
```

### 🎓 Program-Level Officer (Computer Science - NO promotion)
```
Username: cs_officer
Password: CSProgram@123
Organization: Computer Science Student Government
Role: Treasurer
Permissions: Can process payments ONLY
Access: ONLY Computer Science program data
```

### 🌍 Program-Level Officer (Environmental Science - WITH promotion)
```
Username: es_officer
Password: EnvScience@123
Organization: Environmental Science Club
Role: President
Permissions: Can process & void payments, can promote officers
Access: ONLY Environmental Science program data
```

### 👨‍💼 Super Admin
```
Username: admin2
Password: Admin2@12345
Access: EVERYTHING (Django admin + all pages)
```

---

## 📋 Testing Scenarios

### Scenario 1: College-Level Officer Multi-Program Access
**Objective**: Verify college officer can see and manage all programs

**Steps**:
1. Login with `college_officer` / `CollegeOfficer@123`
2. Go to Officer Dashboard
3. Click "Promote Officer" button
4. In the form, open the "Select Student to Promote" dropdown
5. **Expected**: Should see students from ALL three programs (CS, ES, IT)
6. Try selecting students from different programs and assign them to different organizations
7. **Expected**: Should succeed for any program organization

**Success Criteria**:
- ✅ Can access all program data
- ✅ Can promote officers to any program
- ✅ Can demote officers from any program
- ✅ See consolidated reports for entire college

---

### Scenario 2: Program-Level Officer - Limited Access (No Promotion)
**Objective**: Verify program officer has restricted access and no promotion

**Steps**:
1. Login with `cs_officer` / `CSProgram@123`
2. Go to Officer Dashboard
3. **Expected**: Dashboard shows only Computer Science data
4. Try clicking "Promote Officer" in navigation
5. **Expected**: Button should NOT be visible (no can_promote_officers permission)
6. Navigate to `/staff/students/` 
7. **Expected**: Should see ONLY CS program students
8. Try accessing Environmental Science student detail page
9. **Expected**: Should be denied (403 Forbidden)

**Success Criteria**:
- ✅ Cannot see other programs' data
- ✅ Cannot access promote/demote functions
- ✅ Can process payments only
- ✅ Cannot access students from other programs

---

### Scenario 3: Program-Level Officer - WITH Promotion Authority
**Objective**: Verify program officer can promote within their program only

**Steps**:
1. Login with `es_officer` / `EnvScience@123`
2. Go to Officer Dashboard
3. **Expected**: Dashboard shows only Environmental Science data
4. Click "Promote Officer" button in navigation
5. **Expected**: Button IS visible (has can_promote_officers permission)
6. In the form, open "Select Student to Promote" dropdown
7. **Expected**: Should see ONLY ES program students
8. Try selecting a Computer Science student (if any exist)
9. **Expected**: CS students should NOT appear in dropdown
10. Try accessing Computer Science student page directly via URL
11. **Expected**: Should be denied (403 Forbidden)

**Success Criteria**:
- ✅ Can promote officers within their program
- ✅ Can demote officers from their program
- ✅ Cannot see other programs' data
- ✅ Can process & void payments within program
- ✅ Cannot access other programs

---

### Scenario 4: Super Admin Unrestricted Access
**Objective**: Verify super admin has complete access

**Steps**:
1. Login with `admin2` / `Admin2@12345`
2. Navigate to `/admin/` (Django Admin)
3. **Expected**: Can access all models and data
4. Go to student list and view any student
5. **Expected**: Can view and edit any student regardless of program
6. Try promoting/demoting any officer
7. **Expected**: Can succeed for any organization
8. Check organization settings
9. **Expected**: Can modify hierarchy and permissions

**Success Criteria**:
- ✅ Full access to Django admin
- ✅ Can modify any student/officer/organization
- ✅ Can change organization hierarchy
- ✅ No access restrictions

---

## 🔐 Security Verification Tests

Run these tests to verify the organization hierarchy security:

### Test 1: Cross-Program Access Denial
```
1. Login as cs_officer
2. Get a Computer Science student detail page URL
3. Try manually accessing an Environmental Science student URL
4. Expected: 403 Forbidden or 404
```

### Test 2: Promotion Authority Verification
```
1. Login as es_officer (has promotion)
2. Navigate to /staff/officers/promote/
3. Expected: Page loads and can promote
4. Login as cs_officer (no promotion)
5. Navigate to /staff/officers/promote/
6. Expected: Access denied message
```

### Test 3: College Officer Access Expansion
```
1. Create a new student in IT program
2. Login as college_officer
3. Try to promote the IT student
4. Expected: IT student should appear in dropdown
5. Login as cs_officer
6. Try to promote the same IT student
7. Expected: IT student should NOT appear in dropdown
```

### Test 4: Data Isolation
```
As cs_officer:
- /staff/students/ → Should see ~3 CS students
- /staff/officers/ → Should see ~1 CS officer
- /staff/payments/ → Should see only CS payments

As es_officer:
- /staff/students/ → Should see ~3 ES students
- /staff/officers/ → Should see ~1 ES officer
- /staff/payments/ → Should see only ES payments

As college_officer:
- /staff/students/ → Should see ~9 students (all 3 programs)
- /staff/officers/ → Should see ~3 officers (all programs)
- /staff/payments/ → Should see all payments
```

---

## 🎯 Testing Checklist

**For College-Level Officer**:
- [ ] Can see all programs in dropdowns
- [ ] Can assign officers to any program
- [ ] Can demote officers from any program
- [ ] Can process payments from all programs
- [ ] Can generate college-wide reports
- [ ] Cannot access /admin/ (not a superuser)

**For Program-Level Officer (No Promotion)**:
- [ ] Cannot see "Promote Officer" button
- [ ] Cannot access /staff/officers/promote/
- [ ] Can only see their program's students
- [ ] Can only see their program's officers
- [ ] Cannot access other program's data
- [ ] Can process payments only

**For Program-Level Officer (With Promotion)**:
- [ ] CAN see "Promote Officer" button
- [ ] CAN access /staff/officers/promote/
- [ ] Can only promote within their program
- [ ] Can only see their program's students
- [ ] Cannot see other program's data
- [ ] Can process & void payments

**For Super Admin**:
- [ ] Can access /admin/ (full Django admin)
- [ ] Can see all organizations
- [ ] Can see all students across all programs
- [ ] Can modify any officer/student/organization
- [ ] Can change hierarchy structure
- [ ] Can grant/revoke permissions

---

## 📊 Organization Structure Created

```
College of Sciences (COLLEGE LEVEL)
│
├─ College of Sciences Administration
│  └─ college_officer [Can promote, can see all programs]
│
├─ Computer Science
│  ├─ Computer Science Student Government
│  └─ cs_officer [No promotion, CS-only access]
│
├─ Environmental Science
│  ├─ Environmental Science Club
│  └─ es_officer [Can promote, ES-only access]
│
└─ Information Technology
   └─ [No officer yet - can be tested later]
```

---

## 🚀 Running the Test Script

To create these test accounts, run:

```bash
cd projectsite
python create_test_officers.py
```

This will display the hierarchy structure and all credentials.

---

## 💡 Notes for Teammates

1. **College Officer is powerful**: `college_officer` can manage the entire college hierarchy. Start with this account to test high-level permissions.

2. **Program officers have limits**: Test both `cs_officer` (no promotion) and `es_officer` (with promotion) to see the difference in capabilities.

3. **Data filtering is automatic**: The system automatically filters data based on organization hierarchy when these officers access `/staff/` pages.

4. **Promotion respects hierarchy**: When promoting a student, the officer can only assign them to organizations within their accessible hierarchy.

5. **Demotion uses same logic**: Demoting officers respects the same organization hierarchy checks.

6. **Super admin bypasses everything**: `admin2` is the ultimate account for testing and administration.

---

## 🔧 Common Tasks

### Create a Student for Testing
```bash
cd projectsite
python manage.py shell
>>> from paymentorg.models import Student, User, Course
>>> course = Course.objects.get(program_type='COMPUTER_SCIENCE')
>>> user = User.objects.create_user(username='teststudent', password='test123')
>>> student = Student.objects.create(
...     user=user,
...     student_id_number='2024-00001',
...     first_name='Test',
...     last_name='Student',
...     course=course
... )
```

### Change Officer Promotion Authority
```bash
python manage.py shell
>>> from paymentorg.models import Officer
>>> officer = Officer.objects.get(user__username='cs_officer')
>>> officer.can_promote_officers = True
>>> officer.save()
>>> print("cs_officer can now promote officers!")
```

### Add Organization Hierarchy
```bash
python manage.py shell
>>> from paymentorg.models import Organization
>>> parent = Organization.objects.get(code='COSA')
>>> child = Organization.objects.create(
...     name='New Program Organization',
...     code='NEWPROG',
...     hierarchy_level='PROGRAM',
...     parent_organization=parent,
...     # ... other fields
... )
```
