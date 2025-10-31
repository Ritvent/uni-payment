from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import Student, Officer, Organization, FeeType, PaymentRequest, Payment, Receipt, ActivityLog, AcademicYearConfig

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['student_id_number', 'get_full_name', 'course', 'year_level', 'college', 'email']
    list_filter = ['college', 'course', 'year_level', 'academic_year', 'semester']
    search_fields = ['student_id_number', 'first_name', 'last_name', 'email']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Officer)
class OfficerAdmin(admin.ModelAdmin):
    list_display = ['employee_id', 'get_full_name', 'organization', 'role', 'email']
    list_filter = ['organization', 'role']
    search_fields = ['employee_id', 'first_name', 'last_name', 'email']

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'department', 'contact_email', 'booth_location']
    search_fields = ['name', 'code', 'department']

@admin.register(FeeType)
class FeeTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'organization', 'amount', 'academic_year', 'semester', 'deadline']
    list_filter = ['organization', 'academic_year', 'semester']
    search_fields = ['name', 'organization__name']

@admin.register(PaymentRequest)
class PaymentRequestAdmin(admin.ModelAdmin):
    list_display = ['queue_number', 'student', 'organization', 'amount', 'status', 'created_at']
    list_filter = ['status', 'organization', 'created_at']
    search_fields = ['queue_number', 'student__student_id_number']
    readonly_fields = ['request_id', 'created_at', 'updated_at']

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['or_number', 'student', 'organization', 'amount', 'status', 'created_at']
    list_filter = ['status', 'organization', 'payment_method']
    search_fields = ['or_number', 'student__student_id_number']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Receipt)
class ReceiptAdmin(admin.ModelAdmin):
    list_display = ['or_number', 'payment', 'email_sent', 'sms_sent', 'created_at']
    list_filter = ['email_sent', 'sms_sent']
    search_fields = ['or_number']

@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'action', 'created_at']
    list_filter = ['action', 'created_at']
    search_fields = ['user__username', 'action']
    readonly_fields = ['created_at']

@admin.register(AcademicYearConfig)
class AcademicYearConfigAdmin(admin.ModelAdmin):
    list_display = ['academic_year', 'semester', 'start_date', 'end_date', 'is_current']
    list_filter = ['is_current']
    search_fields = ['academic_year']