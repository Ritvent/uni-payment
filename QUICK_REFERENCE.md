# UniPay Organization Hierarchy - Quick Reference

## Test Accounts

| Account | Username | Password | Role | Permissions | Access |
|---------|----------|----------|------|-------------|--------|
| **College Officer** | `college_officer` | `CollegeOfficer@123` | College Admin | Can promote | ALL programs |
| **Program Officer** | `cs_officer` | `CSProgram@123` | Treasurer | Process only | CS only |
| **Program Officer+** | `es_officer` | `EnvScience@123` | President | Can promote | ES only |
| **Super Admin** | `admin2` | `Admin2@12345` | Admin | Full | EVERYTHING |

## Quick Test

### Test 1: Login & Check Navigation
1. Login as `college_officer`
2. Should see **"Promote Officer"** and **"Demote Officer"** in nav
3. Login as `cs_officer`
4. Should NOT see "Promote Officer" button

### Test 2: Promotion Access
1. As `college_officer`: Click "Promote Officer"
2. Student dropdown should show students from **ALL 3 programs** (CS, ES, IT)
3. As `cs_officer`: Cannot access `/staff/officers/promote/`

### Test 3: Data Isolation
1. As `cs_officer`: Go to `/staff/students/`
2. Should see **ONLY** Computer Science students
3. Try accessing ES student URL → **403 Forbidden**

### Test 4: Super Admin
1. Login as `admin2`
2. Access `/admin/` → Full Django admin access
3. Can see all organizations and modify any data

## Hierarchy Structure

```
College of Sciences
├─ college_officer (Can manage all)
│  ├─ cs_officer (CS only)
│  ├─ es_officer (ES only)
│  └─ (IT not assigned yet)
```

## Key Test Scenarios

### ✅ College Officer Should
- [ ] See all programs in dropdowns
- [ ] Promote students from ANY program
- [ ] Access all org data via `/staff/` pages
- [ ] Cannot access `/admin/` (not superuser)

### ✅ CS Officer Should
- [ ] See "Promote Officer" button → **NO** (no permission)
- [ ] Access `/staff/students/` → **Only CS students**
- [ ] Try ES student page → **403 Forbidden**
- [ ] Process payments → **Yes**

### ✅ ES Officer Should
- [ ] See "Promote Officer" button → **YES** (has permission)
- [ ] Promote only ES students → **Yes**
- [ ] Access `/staff/students/` → **Only ES students**
- [ ] Try CS student page → **403 Forbidden**

### ✅ Super Admin Should
- [ ] Access `/admin/` → **Full access**
- [ ] See all organizations → **Yes**
- [ ] Modify any student/officer → **Yes**
- [ ] Change hierarchy → **Yes**

## Files for Reference

- **TESTING_GUIDE.md** - Detailed testing procedures
- **IMPLEMENTATION_SUMMARY.md** - Technical implementation details
- **README.md** - Updated with new credentials

## Run Tests

```bash
cd projectsite
python create_test_officers.py
```

This displays:
- ✅ All test credentials
- ✅ Organization structure
- ✅ Testing scenarios
- ✅ Security tests

## URLs to Test

**With college_officer account:**
- `/officer/dashboard/` - Should show all programs
- `/staff/students/` - Should show students from all programs
- `/staff/officers/` - Should show officers from all programs
- `/staff/officers/promote/` - Can see student dropdown from all programs

**With cs_officer account:**
- `/officer/dashboard/` - Should show only CS data
- `/staff/students/` - Should show only CS students
- `/staff/officers/promote/` - Access denied
- Try accessing ES student URL → 403 Forbidden

**With es_officer account:**
- `/officer/dashboard/` - Should show only ES data
- `/staff/officers/promote/` - Can see ES students only
- `/staff/officers/demote/` - Can see ES officers only
- Cannot promote CS students (not accessible)

**With admin2 account:**
- `/admin/` - Full Django admin
- `/staff/students/` - All students visible
- `/staff/officers/` - All officers visible
- Can modify organization hierarchy

## Success Criteria

✅ **System is working correctly when:**
1. College officer can see all programs
2. Program officers see only their program
3. Promotion respects organization hierarchy
4. Admin has unrestricted access
5. Activity is logged for all actions
6. No cross-organization data leakage

---

## Need Help?

- **Testing questions**: See TESTING_GUIDE.md
- **Implementation details**: See IMPLEMENTATION_SUMMARY.md
- **Features and roadmap**: See README.md
- **Django shell testing**: `python manage.py shell`

---

## Created By
Organization Hierarchy System for UniPay
November 22, 2025
