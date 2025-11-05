from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from django.views.generic import View, ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from .models import Student, Officer, Organization, FeeType, PaymentRequest, Payment, Receipt, ActivityLog
import uuid
from django.http import JsonResponse
from .forms import StudentPaymentRequestForm, OfficerPaymentProcessForm, OrganizationForm, FeeTypeForm, PaymentForm, OfficerForm, StudentForm, PaymentRequestForm, VoidPaymentForm

# home page
class HomePageView(ListView):
    model = Organization
    context_object_name = 'organizations'
    template_name = "home.html"

    def get_queryset(self):
        return Organization.objects.filter(is_active=True)

# show pending payments and available fees
class StudentDashboardView(LoginRequiredMixin, ListView):
    model = PaymentRequest
    context_object_name = 'pending_payments'
    template_name = 'student_dashboard.html'
    
    def get_queryset(self):
        student = get_object_or_404(Student, user=self.request.user)
        return student.payment_requests.filter(status='PENDING')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = get_object_or_404(Student, user=self.request.user)
        
        context['student'] = student
        context['completed_payments'] = Payment.objects.filter(student=student, status='COMPLETED')
        context['available_fees'] = FeeType.objects.filter(
            organization__department=student.college,
            is_active=True
        )
        return context

# show today's payments and pending requests
class OfficerDashboardView(LoginRequiredMixin, ListView):
    model = Payment
    context_object_name = 'today_payments'
    template_name = 'officer_dashboard.html'
    
    def get_queryset(self):
        officer = get_object_or_404(Officer, user=self.request.user)
        today = timezone.now().date()
        return officer.organization.payments.filter(
            created_at__date=today,
            status='COMPLETED'
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        officer = get_object_or_404(Officer, user=self.request.user)
        organization = officer.organization
        
        context['officer'] = officer
        context['organization'] = organization
        context['pending_requests'] = organization.payment_requests.filter(status='PENDING')
        context['total_today'] = sum(payment.amount for payment in self.get_queryset())
        return context

# show active fees for an organization
class OrganizationFeesView(LoginRequiredMixin, ListView):
    model = FeeType
    context_object_name = 'active_fees'
    template_name = 'organization_fees.html'
    
    def get_queryset(self):
        organization = get_object_or_404(Organization, code=self.kwargs['org_code'])
        return organization.fee_types.filter(is_active=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['organization'] = get_object_or_404(Organization, code=self.kwargs['org_code'])
        return context

# show all student payments
class PaymentHistoryView(LoginRequiredMixin, ListView):
    model = Payment
    context_object_name = 'payments'
    template_name = 'payment_history.html'
    
    def get_queryset(self):
        student = get_object_or_404(Student, user=self.request.user)
        return Payment.objects.filter(student=student).order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['student'] = get_object_or_404(Student, user=self.request.user)
        return context

# payment detail view
class PaymentDetailView(LoginRequiredMixin, DetailView):
    model = Payment
    context_object_name = 'payment'
    template_name = 'payment_detail.html'
    
    def get_queryset(self):
        if hasattr(self.request.user, 'student_profile'):
            student = self.request.user.student_profile
            return Payment.objects.filter(student=student)
        elif hasattr(self.request.user, 'officer_profile'):
            officer = self.request.user.officer_profile
            return Payment.objects.filter(organization=officer.organization)
        return Payment.objects.none()

# filter payments by query and date
class SearchPaymentsView(LoginRequiredMixin, ListView):
    model = Payment
    context_object_name = 'payments'
    template_name = 'search_payments.html'
    
    def get_queryset(self):
        officer = get_object_or_404(Officer, user=self.request.user)
        organization = officer.organization
        
        payments = organization.payments.filter(status='COMPLETED')
        
        query = self.request.GET.get('q', '')
        if query:
            payments = payments.filter(
                Q(or_number__icontains=query) |
                Q(student__student_id_number__icontains=query) |
                Q(student__first_name__icontains=query) |
                Q(student__last_name__icontains=query)
            )
        
        date_from = self.request.GET.get('date_from', '')
        if date_from:
            payments = payments.filter(created_at__date__gte=date_from)
        
        date_to = self.request.GET.get('date_to', '')
        if date_to:
            payments = payments.filter(created_at__date__lte=date_to)
        
        return payments.order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        officer = get_object_or_404(Officer, user=self.request.user)
        context['officer'] = officer
        context['organization'] = officer.organization
        context['query'] = self.request.GET.get('q', '')
        context['date_from'] = self.request.GET.get('date_from', '')
        context['date_to'] = self.request.GET.get('date_to', '')
        return context

# generate qr code for payment
class GenerateQRPaymentView(LoginRequiredMixin, CreateView):
    model = PaymentRequest
    form_class = StudentPaymentRequestForm
    template_name = 'generate_qr.html'
    success_url = reverse_lazy('student_dashboard')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = get_object_or_404(Student, user=self.request.user)
        context['available_fees'] = FeeType.objects.filter(
            organization__department=student.college,
            is_active=True
        )
        return context
    
    def form_valid(self, form):
        student = get_object_or_404(Student, user=self.request.user)
        fee_type = form.cleaned_data['fee_type']
        
        # generate unique queue number
        queue_number = f"{fee_type.organization.code}-{student.id:03d}"
        
        # create payment request
        payment_request = form.save(commit=False)
        payment_request.student = student
        payment_request.organization = fee_type.organization
        payment_request.amount = fee_type.amount
        payment_request.queue_number = queue_number
        payment_request.qr_signature = str(uuid.uuid4())
        payment_request.expires_at = timezone.now() + timezone.timedelta(hours=24)
        payment_request.save()
        
        # log activity
        ActivityLog.objects.create(
            user=self.request.user,
            action='qr_generated',
            description=f'student {student.get_full_name()} generated qr for {fee_type.name}',
            payment_request=payment_request
        )
        
        messages.success(self.request, f'qr code generated for {fee_type.name}. queue number: {queue_number}')
        return super().form_valid(form)

# create payment record and receipt
class ProcessPaymentView(LoginRequiredMixin, CreateView):
    model = Payment
    form_class = OfficerPaymentProcessForm
    template_name = 'process_payment.html'
    success_url = reverse_lazy('officer_dashboard')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        officer = get_object_or_404(Officer, user=self.request.user)
        payment_request = get_object_or_404(
            PaymentRequest, 
            request_id=self.kwargs['request_id'],
            status='PENDING'
        )
        context['officer'] = officer
        context['payment_request'] = payment_request
        return context
    
    def form_valid(self, form):
        officer = get_object_or_404(Officer, user=self.request.user)
        payment_request = get_object_or_404(
            PaymentRequest, 
            request_id=self.kwargs['request_id'],
            status='PENDING'
        )
        
        # create payment record
        payment = form.save(commit=False)
        payment.payment_request = payment_request
        payment.student = payment_request.student
        payment.organization = payment_request.organization
        payment.fee_type = payment_request.fee_type
        payment.amount = payment_request.amount
        payment.or_number = f"OR-{uuid.uuid4().hex[:8].upper()}"
        payment.payment_method = 'CASH'
        payment.processed_by = officer
        payment.save()
        
        # update payment request status
        payment_request.mark_as_paid()
        
        # create receipt
        Receipt.objects.create(
            payment=payment,
            or_number=payment.or_number,
            verification_signature=str(uuid.uuid4())
        )
        
        # log activity
        ActivityLog.objects.create(
            user=self.request.user,
            action='payment_processed',
            description=f'officer processed payment OR#{payment.or_number} for {payment.student.get_full_name()}',
            payment=payment,
            payment_request=payment_request
        )
        
        messages.success(self.request, f'payment processed successfully. OR#: {payment.or_number}')
        return super().form_valid(form)

# update paymentrequest status
class CancelPaymentRequestView(LoginRequiredMixin, UpdateView):
    model = PaymentRequest
    form_class = PaymentRequestForm
    template_name = 'cancel_request.html'
    success_url = reverse_lazy('student_dashboard')
    
    def get_object(self):
        student = get_object_or_404(Student, user=self.request.user)
        return get_object_or_404(
            PaymentRequest, 
            request_id=self.kwargs['request_id'], 
            student=student,
            status='PENDING'
        )
    
    def form_valid(self, form):
        payment_request = form.save(commit=False)
        payment_request.mark_as_cancelled()
        
        # log activity
        ActivityLog.objects.create(
            user=self.request.user,
            action='payment_cancelled',
            description=f'student cancelled payment request {payment_request.queue_number}',
            payment_request=payment_request
        )
        
        messages.success(self.request, 'payment request cancelled successfully.')
        return redirect('student_dashboard')

# mark payment as void with reason
class VoidPaymentView(LoginRequiredMixin, UpdateView):
    model = Payment
    form_class = VoidPaymentForm
    template_name = 'void_payment.html'
    success_url = reverse_lazy('officer_dashboard')
    
    def get_object(self):
        officer = get_object_or_404(Officer, user=self.request.user)
        
        if not officer.can_void_payments:
            messages.error(self.request, 'you do not have permission to void payments.')
            return redirect('officer_dashboard')
            
        return get_object_or_404(
            Payment,
            id=self.kwargs['payment_id'],
            organization=officer.organization,
            status='COMPLETED'
        )
    
    def form_valid(self, form):
        officer = get_object_or_404(Officer, user=self.request.user)
        payment = form.save(commit=False)
        
        # update payment status
        payment.mark_as_void(officer, form.cleaned_data['void_reason'])
        
        # log activity
        ActivityLog.objects.create(
            user=self.request.user,
            action='payment_voided',
            description=f'officer voided payment OR#{payment.or_number}. reason: {form.cleaned_data["void_reason"]}',
            payment=payment
        )
        
        messages.success(self.request, f'payment OR#{payment.or_number} has been voided.')
        return redirect('officer_dashboard')

# edit contact information
class UpdateStudentProfileView(LoginRequiredMixin, UpdateView):
    model = Student
    form_class = StudentForm
    template_name = 'update_profile.html'
    success_url = reverse_lazy('student_dashboard')
    
    def get_object(self):
        return get_object_or_404(Student, user=self.request.user)
    
    def form_valid(self, form):
        ActivityLog.objects.create(
            user=self.request.user,
            action='profile_updated',
            description='student updated their profile information'
        )
        messages.success(self.request, 'profile updated successfully.')
        return super().form_valid(form)

# delete payment request
class DeletePaymentRequestView(LoginRequiredMixin, DeleteView):
    model = PaymentRequest
    template_name = 'delete_request.html'
    success_url = reverse_lazy('student_dashboard')
    
    def get_object(self):
        student = get_object_or_404(Student, user=self.request.user)
        return get_object_or_404(
            PaymentRequest, 
            request_id=self.kwargs['request_id'], 
            student=student,
            status='PENDING'
        )
    
    def delete(self, request, *args, **kwargs):
        payment_request = self.get_object()
        
        # log activity before deletion
        ActivityLog.objects.create(
            user=request.user,
            action='payment_request_deleted',
            description=f'student deleted payment request {payment_request.queue_number}',
            payment_request=payment_request
        )
        
        messages.success(request, 'payment request deleted successfully.')
        return super().delete(request, *args, **kwargs)

# return json data for student payments status
class PaymentStatusAPIView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        try:
            student = Student.objects.get(user=request.user)
            pending_count = student.get_pending_payments_count()
            recent_payments = student.get_completed_payments()[:5]
            
            data = {
                'pending_count': pending_count,
                'recent_payments': [
                    {
                        'or_number': payment.or_number,
                        'organization': payment.organization.name,
                        'amount': float(payment.amount),
                        'date': payment.created_at.isoformat()
                    }
                    for payment in recent_payments
                ]
            }
            return JsonResponse(data)
        except Student.DoesNotExist:
            return JsonResponse({'error': 'student profile not found'}, status=404)

# organization crud views
class CreateOrganizationView(LoginRequiredMixin, CreateView):
    model = Organization
    form_class = OrganizationForm
    template_name = 'create_organization.html'
    success_url = reverse_lazy('home')

class UpdateOrganizationView(LoginRequiredMixin, UpdateView):
    model = Organization
    form_class = OrganizationForm
    template_name = 'update_organization.html'
    success_url = reverse_lazy('home')

class DeleteOrganizationView(LoginRequiredMixin, DeleteView):
    model = Organization
    template_name = 'delete_organization.html'
    success_url = reverse_lazy('home')

# feetype crud views
class CreateFeeTypeView(LoginRequiredMixin, CreateView):
    model = FeeType
    form_class = FeeTypeForm
    template_name = 'create_feetype.html'
    success_url = reverse_lazy('home')

class UpdateFeeTypeView(LoginRequiredMixin, UpdateView):
    model = FeeType
    form_class = FeeTypeForm
    template_name = 'update_feetype.html'
    success_url = reverse_lazy('home')

class DeleteFeeTypeView(LoginRequiredMixin, DeleteView):
    model = FeeType
    template_name = 'delete_feetype.html'
    success_url = reverse_lazy('home')

# officer crud views
class CreateOfficerView(LoginRequiredMixin, CreateView):
    model = Officer
    form_class = OfficerForm
    template_name = 'create_officer.html'
    success_url = reverse_lazy('home')

class UpdateOfficerView(LoginRequiredMixin, UpdateView):
    model = Officer
    form_class = OfficerForm
    template_name = 'update_officer.html'
    success_url = reverse_lazy('home')

class DeleteOfficerView(LoginRequiredMixin, DeleteView):
    model = Officer
    template_name = 'delete_officer.html'
    success_url = reverse_lazy('home')

# student crud views
class CreateStudentView(LoginRequiredMixin, CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'create_student.html'
    success_url = reverse_lazy('home')

class DeleteStudentView(LoginRequiredMixin, DeleteView):
    model = Student
    template_name = 'delete_student.html'
    success_url = reverse_lazy('home')

# payment crud views
class CreatePaymentView(LoginRequiredMixin, CreateView):
    model = Payment
    form_class = PaymentForm
    template_name = 'create_payment.html'
    success_url = reverse_lazy('home')

class UpdatePaymentView(LoginRequiredMixin, UpdateView):
    model = Payment
    form_class = PaymentForm
    template_name = 'update_payment.html'
    success_url = reverse_lazy('home')

class DeletePaymentView(LoginRequiredMixin, DeleteView):
    model = Payment
    template_name = 'delete_payment.html'
    success_url = reverse_lazy('home')