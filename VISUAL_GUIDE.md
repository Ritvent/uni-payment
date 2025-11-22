# Organization Hierarchy - Visual Guide

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    UNIPAY SYSTEM                                │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │           AUTHENTICATION LAYER                           │  │
│  │  Single login → User → Student & Officer profiles       │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │      ORGANIZATION HIERARCHY (NEW)                        │  │
│  │                                                          │  │
│  │    College of Sciences (HIERARCHY_LEVEL = COLLEGE)       │  │
│  │    parent_organization = NULL                           │  │
│  │    ├─ College of Sciences Admin                         │  │
│  │    │  └─ can_promote_officers = TRUE                   │  │
│  │    │                                                    │  │
│  │    └─ Program Organizations (HIERARCHY_LEVEL = PROGRAM)│  │
│  │       parent_organization = College of Sciences        │  │
│  │       ├─ Computer Science Student Gov                  │  │
│  │       │  └─ can_promote_officers = FALSE              │  │
│  │       ├─ Environmental Science Club                    │  │
│  │       │  └─ can_promote_officers = TRUE               │  │
│  │       └─ IT (no officer yet)                           │  │
│  │                                                        │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │        PERMISSION & ACCESS CONTROL LAYER                │  │
│  │                                                          │  │
│  │  college_officer:                                       │  │
│  │  ├─ can_promote_officers = TRUE                        │  │
│  │  ├─ is_super_officer = FALSE                           │  │
│  │  └─ Accessible Orgs = self + all children             │  │
│  │     (College + CS + ES + IT)                          │  │
│  │                                                          │  │
│  │  cs_officer:                                            │  │
│  │  ├─ can_promote_officers = FALSE                       │  │
│  │  ├─ is_super_officer = FALSE                           │  │
│  │  └─ Accessible Orgs = self only (CS)                  │  │
│  │                                                          │  │
│  │  es_officer:                                            │  │
│  │  ├─ can_promote_officers = TRUE                        │  │
│  │  ├─ is_super_officer = FALSE                           │  │
│  │  └─ Accessible Orgs = self only (ES)                  │  │
│  │                                                          │  │
│  │  admin2 (superuser):                                    │  │
│  │  ├─ is_staff = TRUE                                    │  │
│  │  ├─ is_superuser = TRUE                                │  │
│  │  └─ Accessible Orgs = ALL                              │  │
│  │                                                          │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │           FEATURE ACCESS MATRIX                          │  │
│  │                                                          │  │
│  │                 │ College │  CS    │  ES    │ Admin   │  │
│  │─────────────────┼─────────┼────────┼────────┼─────────┤  │
│  │ Promote Officer │   ✅    │   ❌   │   ✅   │   ✅    │  │
│  │ Demote Officer  │   ✅    │   ❌   │   ✅   │   ✅    │  │
│  │ View Students   │   All   │  CS    │   ES   │   All   │  │
│  │ View Officers   │   All   │  CS    │   ES   │   All   │  │
│  │ Process Payment │   ✅    │   ✅   │   ✅   │   ✅    │  │
│  │ Void Payment    │   ✅    │   ❌   │   ✅   │   ✅    │  │
│  │ Django Admin    │   ❌    │   ❌   │   ❌   │   ✅    │  │
│  │                                                          │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow Diagram

```
┌──────────────────┐
│  Officer Login   │
└────────┬─────────┘
         │
         v
┌──────────────────────────────────┐
│ Check Officer.can_promote_officers│
└────────┬───────────┬─────────────┘
         │           │
      YES│           │NO
         v           v
    Show Promote   Hide Promote
    & Demote       & Demote
    Buttons        Buttons
         │           │
         └─────┬─────┘
               v
    ┌──────────────────────┐
    │ Officer Dashboard    │
    └──────────┬───────────┘
               │
               v
    ┌──────────────────────────────┐
    │ Get Accessible Organizations │
    │ (self + all children)        │
    └──────────┬───────────────────┘
               │
               v
    ┌──────────────────────────────┐
    │ Filter View Querysets        │
    │ by org_id IN accessible_ids  │
    └──────────┬───────────────────┘
               │
         ┌─────┴──────────┬─────────────┐
         │                │             │
         v                v             v
    Students        Officers      Payments
    (filtered)      (filtered)    (filtered)
         │                │             │
         └─────────┬──────┴─────┬───────┘
                   v            v
            Display in     Display in
            Templates      Reports
```

## Permission Decision Tree

```
                    User Makes Request
                            │
                            v
                   Is User Authenticated?
                    /          \
                  NO            YES
                  │              │
            Redirect to      v
            Login        Is User Superuser?
                          /        \
                        YES        NO
                        │           │
                    Grant       v
                   Access   Does User Have
                            Officer Profile?
                            /          \
                          NO           YES
                          │             │
                        Deny        v
                       Access   Is User Trying to
                                Promote/Demote?
                                /            \
                              NO             YES
                              │               │
                          Check if        v
                        can access       Does Officer Have
                        this org        can_promote_officers?
                        /      \         /          \
                      YES      NO      YES          NO
                      │        │       │            │
                    View    403    Allow       Access
                    Data   Error  Function    Denied
```

## Organization Tree Traversal

```
get_accessible_organizations() for college_officer:

college_org.get_accessible_organizations()
    │
    ├─ Returns: [college_org]
    │ 
    └─ Calls: get_all_child_organizations()
        │
        ├─ Gets: cs_org, es_org, it_org
        │ 
        ├─ For each child, recursively calls:
        │  get_all_child_organizations()
        │   (No further children, returns [])
        │
        └─ Returns: [cs_org, es_org, it_org]

Final Result: [college_org, cs_org, es_org, it_org]

ID List for Query Filter:
org_id IN (1, 2, 3, 4)  # All accessible organizations
```

## Promotion Workflow

```
Officer Clicks "Promote Officer"
         │
         v
   Load Promotion Form
         │
         v
   Get Officer's Accessible Organizations
   college_officer: [all 4]
   cs_officer: [cs_org only]
   es_officer: [es_org only]
         │
         v
   Filter Students by Accessible Orgs
   college_officer: Students from all programs
   cs_officer: Students from CS only
   es_officer: Students from ES only
         │
         v
   Officer Selects Student & Organization
         │
         v
   Validate Organization is Accessible
         │
    NO   │   YES
        │    │
      Deny  v
      Error Create Officer
             Update UserProfile
             Log Activity
             │
             v
         Redirect to Login
         Show Success Message
```

## Access Control Matrix for Views

```
View: /staff/students/

SuperAdmin:
  queryset = Student.objects.all()  (no filter)
  │
  Displays: All students

college_officer:
  org_ids = [college_org.id, cs_org.id, es_org.id, it_org.id]
  queryset = Student.objects.filter(course__college_id__in=org_ids)
  │
  Displays: ~9 students (3 per program × 3 programs)

cs_officer:
  org_ids = [cs_org.id]
  queryset = Student.objects.filter(course__college_id=cs_org.id)
  │
  Displays: ~3 students (CS only)

es_officer:
  org_ids = [es_org.id]
  queryset = Student.objects.filter(course__college_id=es_org.id)
  │
  Displays: ~3 students (ES only)

Regular Officer (no access):
  test_func() returns False
  │
  Displays: Access Denied → Redirect to Login
```

## Database Relationships

```
┌──────────────────────────────────────────┐
│            User (Django)                 │
├──────────────────────────────────────────┤
│ id, username, password, email            │
└────┬────────────────────────────┬────────┘
     │                            │
     v                            v
┌──────────────────┐      ┌──────────────────┐
│   UserProfile    │      │   Officer        │
├──────────────────┤      ├──────────────────┤
│ user_id (1-1)    │      │ user_id (1-1)    │
│ is_officer       │      │ organization_id  │
│ created_at       │      │ can_promote      │
└──────────────────┘      │ is_super_officer │
                          │ can_void_payment │
                          │ created_at       │
                          └────────┬─────────┘
                                   │
                                   v
                          ┌──────────────────┐
                          │  Organization    │
                          ├──────────────────┤
                          │ id               │
                          │ name             │
                          │ hierarchy_level  │
                          │ parent_org_id    │
                          │ fee_tier         │
                          │ created_at       │
                          └────────┬─────────┘
                                   │
                       ┌───────────┴────────────┐
                       │ (self-referencing)     │
                       │ Can have parent        │
                       │ Can have children      │
                       │                        │
                       └────────────────────────┘
```

## Test Scenario Visualization

```
COLLEGE HIERARCHY TEST:

college_officer login
    ↓
Navigate to /staff/students/
    ↓
Query: Student.objects.filter(
    course__college__organization__in=
        [all accessible orgs]
)
    ↓
Display:
    Computer Science
    ├─ student_cs_001
    ├─ student_cs_002
    └─ student_cs_003
    
    Environmental Science
    ├─ student_es_001
    ├─ student_es_002
    └─ student_es_003
    
    Information Technology
    ├─ student_it_001
    └─ ...


PROGRAM OFFICER TEST:

cs_officer login
    ↓
Navigate to /staff/students/
    ↓
Query: Student.objects.filter(
    course__college__organization_id=
        [cs_org.id only]
)
    ↓
Display:
    Computer Science
    ├─ student_cs_001
    ├─ student_cs_002
    └─ student_cs_003
    
    (No other programs shown)
    
Try accessing:
  /staff/students/<es_student_id>/
    ↓
Check: es_student.organization_id in [cs_org.id]?
    ↓
NO → Return 404 / 403
```

---

## Summary

**The system uses a 3-layer approach:**

1. **Hierarchy Layer** - Organization tree with parent-child relationships
2. **Permission Layer** - Officers with selective promotion authority
3. **Access Layer** - Automatic filtering of querysets based on accessible organizations

This ensures:
- ✅ College officers see all programs
- ✅ Program officers see only their program
- ✅ Promotion respects hierarchy
- ✅ Data is never leaked between organizations
- ✅ Admin has unrestricted access
