from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils import timezone
from django.utils.safestring import mark_safe
from .models import Student, Officer, Organization, FeeType, PaymentRequest, Payment, Receipt, ActivityLog, AcademicYearConfig

# student admin with enhanced display
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['student_id_number', 'get_full_name_display', 'course', 'year_level', 'college', 'pending_payments_count', 'is_active']
    list_filter = ['college', 'course', 'year_level', 'academic_year', 'semester', 'is_active']
    search_fields = ['student_id_number', 'first_name', 'last_name', 'email']
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ['is_active']
    
    def get_full_name_display(self, obj):
        return obj.get_full_name()
    get_full_name_display.short_description = 'full name'
    
    def pending_payments_count(self, obj):
        count = obj.get_pending_payments_count()
        return format_html('<span style="color: {};">{}</span>', 'red' if count > 0 else 'green', count)
    pending_payments_count.short_description = 'pending payments'

# officer admin with permission display
@admin.register(Officer)
class OfficerAdmin(admin.ModelAdmin):
    list_display = ['employee_id', 'get_full_name_display', 'organization', 'role', 'can_process_payments', 'can_void_payments', 'is_active']
    list_filter = ['organization', 'role', 'can_process_payments', 'can_void_payments', 'is_active']
    search_fields = ['employee_id', 'first_name', 'last_name', 'email']
    list_editable = ['can_process_payments', 'can_void_payments', 'is_active']
    
    def get_full_name_display(self, obj):
        return obj.get_full_name()
    get_full_name_display.short_description = 'full name'

# organization admin with financial overview
@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'department', 'active_fees_count', 'total_collected', 'today_collection', 'pending_requests_count', 'is_active']
    search_fields = ['name', 'code', 'department']
    list_filter = ['department', 'is_active']
    list_editable = ['is_active']
    
    def active_fees_count(self, obj):
        return obj.get_active_fees_count()
    active_fees_count.short_description = 'active fees'
    
    def total_collected(self, obj):
        total = obj.get_total_collected()
        return format_html('<b>₱{}</b>', total)
    total_collected.short_description = 'total collected'
    
    def today_collection(self, obj):
        today = obj.get_today_collection()
        return format_html('₱{}', today)
    today_collection.short_description = 'today collected'
    
    def pending_requests_count(self, obj):
        count = obj.get_pending_requests_count()
        return format_html('<span style="color: {};">{}</span>', 'orange' if count > 0 else 'green', count)
    pending_requests_count.short_description = 'pending requests'

# fee type admin with overdue status
@admin.register(FeeType)
class FeeTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'organization', 'amount', 'academic_year', 'semester', 'is_overdue_display', 'is_active']
    list_filter = ['organization', 'academic_year', 'semester', 'is_active']
    search_fields = ['name', 'organization__name']
    list_editable = ['is_active']
    
    def is_overdue_display(self, obj):
        overdue = obj.is_overdue()
        return format_html(
            '<span style="color: {};">{}</span>',
            'red' if overdue else 'green',
            'yes' if overdue else 'no'
        )
    is_overdue_display.boolean = False
    is_overdue_display.short_description = 'overdue'

# payment request admin with status indicators
@admin.register(PaymentRequest)
class PaymentRequestAdmin(admin.ModelAdmin):
    list_display = ['queue_number', 'student_info', 'organization', 'fee_type', 'amount', 'status_display', 'created_at', 'is_expired_display', 'is_active']
    list_filter = ['status', 'organization', 'created_at', 'is_active']
    search_fields = ['queue_number', 'student__student_id_number', 'student__first_name']
    readonly_fields = ['request_id', 'created_at', 'updated_at', 'expires_at']
    list_editable = ['is_active']
    
    def student_info(self, obj):
        return f"{obj.student.student_id_number} - {obj.student.get_full_name()}"
    student_info.short_description = 'student'
    
    def is_expired_display(self, obj):
        expired = obj.is_expired()
        return format_html(
            '<span style="color: {};">{}</span>',
            'red' if expired else 'green',
            'yes' if expired else 'no'
        )
    is_expired_display.short_description = 'expired'
    
    def status_display(self, obj):
        color_map = {
            'PENDING': 'orange',
            'PAID': 'green',
            'CANCELLED': 'gray',
            'EXPIRED': 'red'
        }
        return format_html(
            '<span style="color: {};"><b>{}</b></span>',
            color_map.get(obj.status, 'black'),
            obj.status
        )
    status_display.short_description = 'status'

    def mark_as_paid(modeladmin, request, queryset):
        queryset.update(status='PAID', paid_at=timezone.now())
    mark_as_paid.short_description = "Mark selected as paid"

    actions = [mark_as_paid]

# payment admin with void status
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['or_number', 'student_info', 'organization', 'amount', 'payment_method', 'status_display', 'created_at', 'is_void', 'is_active']
    list_filter = ['status', 'payment_method', 'organization', 'created_at', 'is_void', 'is_active']
    search_fields = ['or_number', 'student__student_id_number']
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ['is_active']
    
    def student_info(self, obj):
        return f"{obj.student.student_id_number} - {obj.student.get_full_name()}"
    student_info.short_description = 'student'
    
    def status_display(self, obj):
        color = 'red' if obj.is_void else 'green'
        status_text = 'void' if obj.is_void else obj.status.lower()
        return format_html(
            '<span style="color: {};"><b>{}</b></span>',
            color,
            status_text
        )
    status_display.short_description = 'status'

# receipt admin with delivery status
@admin.register(Receipt)
class ReceiptAdmin(admin.ModelAdmin):
    list_display = ['or_number', 'payment_info', 'email_sent', 'sms_sent', 'created_at', 'is_active']
    list_filter = ['email_sent', 'sms_sent', 'created_at', 'is_active']
    search_fields = ['or_number']
    list_editable = ['is_active']
    
    def payment_info(self, obj):
        return f"{obj.payment.student.get_full_name()} - ₱{obj.payment.amount}"
    payment_info.short_description = 'payment'

# activity log admin with compact display
@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'action', 'description_short', 'created_at', 'is_active']
    list_filter = ['action', 'created_at', 'is_active']
    search_fields = ['user__username', 'action', 'description']
    readonly_fields = ['created_at']
    list_editable = ['is_active']
    
    def description_short(self, obj):
        return obj.description[:50] + "..." if len(obj.description) > 50 else obj.description
    description_short.short_description = 'description'

# academic year config admin
@admin.register(AcademicYearConfig)
class AcademicYearConfigAdmin(admin.ModelAdmin):
    list_display = ['academic_year', 'semester', 'start_date', 'end_date', 'is_current', 'is_active']
    list_filter = ['is_current', 'academic_year', 'is_active']
    search_fields = ['academic_year', 'semester']
    list_editable = ['is_active']