from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from decimal import Decimal
from .models import Student, Organization, FeeType, PaymentRequest, Payment, Officer

class StudentPaymentRequestForm(forms.ModelForm):
    class Meta:
        model = PaymentRequest
        fields = ['fee_type']
        widgets = {
            'fee_type': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_fee_type(self):
        fee_type = self.cleaned_data['fee_type']
        return fee_type

class OfficerPaymentProcessForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['amount_received', 'payment_method', 'or_number', 'notes']
        widgets = {
            'amount_received': forms.NumberInput(attrs={
                'class': 'form-control', 
                'step': '0.01',
                'min': '0.01',
                'id': 'amount_received'
            }),
            'payment_method': forms.Select(attrs={'class': 'form-control'}),
            'or_number': forms.TextInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'optional notes...'}),
        }

    def clean_amount_received(self):
        amount_received = self.cleaned_data['amount_received']
        if amount_received <= Decimal('0.00'):
            raise ValidationError("amount received must be greater than 0.")
        return amount_received

    def clean_or_number(self):
        or_number = self.cleaned_data['or_number']
        if Payment.objects.filter(or_number=or_number).exists():
            raise ValidationError("or number already exists.")
        return or_number

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['phone_number', 'email', 'course', 'year_level', 'college']
        widgets = {
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'course': forms.TextInput(attrs={'class': 'form-control'}),
            'year_level': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5}),
            'college': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_year_level(self):
        year_level = self.cleaned_data['year_level']
        if year_level < 1 or year_level > 5:
            raise ValidationError("year level must be between 1 and 5.")
        return year_level

class PaymentRequestForm(forms.ModelForm):
    class Meta:
        model = PaymentRequest
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ['name', 'code', 'department', 'description', 'contact_email', 'contact_phone', 'booth_location']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'contact_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'contact_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'booth_location': forms.TextInput(attrs={'class': 'form-control'}),
        }

class FeeTypeForm(forms.ModelForm):
    class Meta:
        model = FeeType
        fields = ['organization', 'name', 'amount', 'description', 'academic_year', 'semester', 'applicable_year_levels', 'deadline']
        widgets = {
            'organization': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'academic_year': forms.TextInput(attrs={'class': 'form-control'}),
            'semester': forms.Select(attrs={'class': 'form-control'}),
            'applicable_year_levels': forms.TextInput(attrs={'class': 'form-control'}),
            'deadline': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['amount_received', 'payment_method', 'or_number', 'notes']
        widgets = {
            'amount_received': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'payment_method': forms.Select(attrs={'class': 'form-control'}),
            'or_number': forms.TextInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

class OfficerForm(forms.ModelForm):
    class Meta:
        model = Officer
        fields = ['employee_id', 'first_name', 'last_name', 'organization', 'role', 'email', 'phone_number']
        widgets = {
            'employee_id': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'organization': forms.Select(attrs={'class': 'form-control'}),
            'role': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
        }

class VoidPaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['void_reason']
        widgets = {
            'void_reason': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3,
                'placeholder': 'enter reason for voiding this payment...'
            }),
        }

    def clean_void_reason(self):
        void_reason = self.cleaned_data['void_reason']
        if not void_reason or len(void_reason.strip()) < 10:
            raise ValidationError("please provide a detailed reason for voiding (at least 10 characters).")
        return void_reason