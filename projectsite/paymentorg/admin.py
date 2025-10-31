from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import Student, Officer,Organization, FeeType, PaymentRequest, Payment, Receipt, ActivityLog,AcademicYearConfig

admin.site.register(Student)
admin.site.register(Officer)
admin.site.register(Organization)
admin.site.register(FeeType)
admin.site.register(PaymentRequest)
admin.site.register(Payment)
admin.site.register(Receipt)
admin.site.register(ActivityLog)
admin.site.register(AcademicYearConfig)



#Register your models here