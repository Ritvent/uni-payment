from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.utils import timezone
from decimal import Decimal
import uuid
# Create your models here.


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True,verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True,verbose_name="Updated At")
    is_active = models.BooleanField(default=True,verbose_name="Is Active")

    class Meta:
        abstract = True
        ordering = ['-created_at']



# USER PROFILE MODELS



class Student(BaseModel):
###################################################333
    # Student profile linked to Django User
    #########################################
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='student_profile'
    )
    student_id_number = models.CharField(
        max_length=20, 
        unique=True, 
        verbose_name="Student ID Number",
        help_text="University student ID (e.g., 2021-12345)"
    )
    first_name = models.CharField(max_length=100, verbose_name="First Name")
    last_name = models.CharField(max_length=100, verbose_name="Last Name")
    middle_name = models.CharField(
        max_length=100, 
        blank=True, 
        null=True, 
        verbose_name="Middle Name"
    )
    
    # Academic Information
    course = models.CharField(
        max_length=100, 
        verbose_name="Course/Program",
        help_text="e.g., BS Biology, BS Chemistry"
    )
    year_level = models.IntegerField(
        validators=[MinValueValidator(1)],
        verbose_name="Year Level",
        help_text="1, 2, 3, 4, or 5"
    )
    college = models.CharField(
        max_length=100,
        verbose_name="College/Department",
        default="College of Sciences"
    )
    
    # Contact Information
    email = models.EmailField(unique=True, verbose_name="Email Address")
    phone_number = models.CharField(
        max_length=15, 
        verbose_name="Phone Number",
        help_text="Format: 09XX-XXX-XXXX"
    )
    
    # Enrollment Info
    academic_year = models.CharField(
        max_length=20,
        verbose_name="Academic Year",
        help_text="e.g., 2024-2025",
        default="2024-2025"
    )
    semester = models.CharField(
        max_length=20,
        verbose_name="Current Semester",
        choices=[
            ('1st Semester', '1st Semester'),
            ('2nd Semester', '2nd Semester'),
            ('Summer', 'Summer'),
        ],
        default='1st Semester'
    )

    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Students"
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.student_id_number} - {self.get_full_name()}"

    def get_full_name(self):
        """Return full name with middle initial"""
        if self.middle_name:
            return f"{self.first_name} {self.middle_name[0]}. {self.last_name}"
        return f"{self.first_name} {self.last_name}"

    def get_pending_payments_count(self):
        """Get count of unpaid fees"""
        return self.payment_requests.filter(status='PENDING').count()