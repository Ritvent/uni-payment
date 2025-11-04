from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from django.views.generic import View, ListView, CreateView, UpdateView, DeleteView, DetailView, TemplateView
from django.urls import reverse_lazy
from .models import Student, Officer, Organization, FeeType, PaymentRequest, Payment, Receipt, ActivityLog
import uuid
from django.http import JsonResponse, Http404
import qrcode
import io
import base64
from django.core.files.base import ContentFile

# home page
class HomePageView(TemplateView):
    template_name = "home.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['organizations'] = Organization.objects.filter(is_active=True)
        return context

# show pending payments and available fees
class StudentDashboardView(LoginRequiredMixin, ListView):
    model = PaymentRequest
    context_object_name = 'pending_payments'
    template_name = 'paymentorg/student_dashboard.html'
    
    def get_queryset(self):
        try:
            student = Student.objects.get(user=self.request.user)
            return student.payment_requests.filter(status='PENDING')
        except Student.DoesNotExist:
            messages.error(self.request, "Student profile not found. Please contact administrator.")
            return PaymentRequest.objects.none()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            student = Student.objects.get(user=self.request.user)
            context['student'] = student
            context['completed_payments'] = Payment.objects.filter(student=student, status='COMPLETED')
            context['available_fees'] = FeeType.objects.filter(
                organization__department=student.college,
                is_active=True
            )
        except Student.DoesNotExist:
            context['student'] = None
            context['completed_payments'] = Payment.objects.none()
            context['available_fees'] = FeeType.objects.none()
        return context

# show today's payments and pending requests
class OfficerDashboardView(LoginRequiredMixin, ListView):
    model = Payment
    context_object_name = 'today_payments'
    template_name = 'paymentorg/officer_dashboard.html'
    
    def get_queryset(self):
        try:
            officer = Officer.objects.get(user=self.request.user)
            today = timezone.now().date()
            return officer.organization.payments.filter(
                created_at__date=today,
                status='COMPLETED'
            )
        except Officer.DoesNotExist:
            messages.error(self.request, "Officer profile not found. Please contact administrator.")
            return Payment.objects.none()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            officer = Officer.objects.get(user=self.request.user)
            organization = officer.organization
            
            context['officer'] = officer
            context['organization'] = organization
            context['pending_requests'] = organization.payment_requests.filter(status='PENDING')
            context['total_today'] = sum(payment.amount for payment in self.get_queryset())
        except Officer.DoesNotExist:
            context['officer'] = None
            context['organization'] = None
            context['pending_requests'] = PaymentRequest.objects.none()
            context['total_today'] = 0
        return context

# show active fees for an organization
class OrganizationFeesView(ListView):
    model = FeeType
    context_object_name = 'active_fees'
    template_name = 'paymentorg/organization_fees.html'
    
    def get_queryset(self):
        try:
            organization = Organization.objects.get(code=self.kwargs['org_code'])
            return organization.fee_types.filter(is_active=True)
        except Organization.DoesNotExist:
            raise Http404("Organization not found.")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['organization'] = Organization.objects.get(code=self.kwargs['org_code'])
        except Organization.DoesNotExist:
            raise Http404("Organization not found.")
        return context

# show all student payments
class PaymentHistoryView(LoginRequiredMixin, ListView):
    model = Payment
    context_object_name = 'payments'
    template_name = 'paymentorg/payment_history.html'
    
    def get_queryset(self):
        try:
            student = Student.objects.get(user=self.request.user)
            return Payment.objects.filter(student=student).order_by('-created_at')
        except Student.DoesNotExist:
            messages.error(self.request, "Student profile not found.")
            return Payment.objects.none()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['student'] = Student.objects.get(user=self.request.user)
        except Student.DoesNotExist:
            context['student'] = None
        return context

# payment detail view
class PaymentDetailView(LoginRequiredMixin, DetailView):
    model = Payment
    context_object_name = 'payment'
    template_name = 'paymentorg/payment_detail.html'
    
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
    template_name = 'paymentorg/search_payments.html'
    
    def get_queryset(self):
        try:
            officer = Officer.objects.get(user=self.request.user)
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
        except Officer.DoesNotExist:
            messages.error(self.request, "Officer profile not found.")
            return Payment.objects.none()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            officer = Officer.objects.get(user=self.request.user)
            context['officer'] = officer
            context['organization'] = officer.organization
            context['query'] = self.request.GET.get('q', '')
            context['date_from'] = self.request.GET.get('date_from', '')
            context['date_to'] = self.request.GET.get('date_to', '')
        except Officer.DoesNotExist:
            context['officer'] = None
            context['organization'] = None
            context['query'] = ''
            context['date_from'] = ''
            context['date_to'] = ''
        return context

# generate QR code for payment
class GenerateQRPaymentView(LoginRequiredMixin, CreateView):
    model = PaymentRequest
    fields = []  # We'll handle creation manually
    template_name = 'paymentorg/generate_qr.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            student = Student.objects.get(user=self.request.user)
            context['available_fees'] = FeeType.objects.filter(
                organization__department=student.college,
                is_active=True
            )
        except Student.DoesNotExist:
            messages.error(self.request, "Student profile not found. Please contact administrator.")
            context['available_fees'] = FeeType.objects.none()
        return context
    
    def post(self, request, *args, **kwargs):
        try:
            student = Student.objects.get(user=request.user)
            fee_type_id = request.POST.get('fee_type')
            fee_type = FeeType.objects.get(id=fee_type_id)
            
            # generate unique queue number
            queue_number = f"{fee_type.organization.code}-{student.id:03d}"
            
            # create QR code data
            qr_signature = str(uuid.uuid4())
            qr_data = f"PAYMENT:{fee_type.organization.code}:{student.student_id_number}:{fee_type.amount}:{qr_signature}"
            
            # generate QR code image
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(qr_data)
            qr.make(fit=True)
            
            qr_img = qr.make_image(fill_color="black", back_color="white")
            
            # save QR code to bytes
            buffer = io.BytesIO()
            qr_img.save(buffer, format='PNG')
            buffer.seek(0)
            
            # create payment request with QR code image
            payment_request = PaymentRequest(
                student=student,
                organization=fee_type.organization,
                fee_type=fee_type,
                amount=fee_type.amount,
                queue_number=queue_number,
                qr_signature=qr_signature,
                expires_at=timezone.now() + timezone.timedelta(hours=24)
            )
            
            # save QR code image to model
            payment_request.qr_code_image.save(
                f'qr_{payment_request.request_id}.png',
                ContentFile(buffer.getvalue())
            )
            payment_request.save()
            
            # generate base64 for immediate display
            buffer.seek(0)
            qr_base64 = base64.b64encode(buffer.getvalue()).decode()
            
            # log activity
            ActivityLog.objects.create(
                user=request.user,
                action='QR_GENERATED',
                description=f'Student {student.get_full_name()} generated QR for {fee_type.name}',
                payment_request=payment_request
            )
            
            # pass QR code to template for display
            context = {
                'payment_request': payment_request,
                'qr_code_data': qr_data,
                'qr_image_base64': qr_base64,
                'queue_number': queue_number
            }
            
            messages.success(request, f'QR code generated for {fee_type.name}. Queue number: {queue_number}')
            return render(request, 'paymentorg/display_qr.html', context)
            
        except Student.DoesNotExist:
            messages.error(request, 'Student profile not found.')
            return redirect('home')
        except FeeType.DoesNotExist:
            messages.error(request, 'Fee type not found.')
            return redirect('generate_qr')
        except Exception as e:
            messages.error(request, f'Error generating QR code: {str(e)}')
            return redirect('student_dashboard')

# create payment record and receipt (CREATE Payment & Receipt)
class ProcessPaymentView(LoginRequiredMixin, CreateView):
    model = Payment
    fields = ['amount_received']
    template_name = 'paymentorg/process_payment.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            officer = Officer.objects.get(user=self.request.user)
            payment_request = PaymentRequest.objects.get(
                request_id=self.kwargs['request_id'],
                status='PENDING'
            )
            context['officer'] = officer
            context['payment_request'] = payment_request
        except Officer.DoesNotExist:
            messages.error(self.request, "Officer profile not found.")
        except PaymentRequest.DoesNotExist:
            messages.error(self.request, "Payment request not found or already processed.")
        return context
    
    def form_valid(self, form):
        try:
            officer = Officer.objects.get(user=self.request.user)
            payment_request = PaymentRequest.objects.get(
                request_id=self.kwargs['request_id'],
                status='PENDING'
            )
            
            # create payment record
            payment = Payment.objects.create(
                payment_request=payment_request,
                student=payment_request.student,
                organization=payment_request.organization,
                fee_type=payment_request.fee_type,
                amount=payment_request.amount,
                amount_received=form.cleaned_data['amount_received'],
                or_number=f"OR-{uuid.uuid4().hex[:8].upper()}",
                payment_method='CASH',
                processed_by=officer
            )
            
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
                action='PAYMENT_PROCESSED',
                description=f'Officer processed payment OR#{payment.or_number} for {payment.student.get_full_name()}',
                payment=payment,
                payment_request=payment_request
            )
            
            messages.success(self.request, f'Payment processed successfully. OR#: {payment.or_number}')
            return redirect('officer_dashboard')
            
        except (Officer.DoesNotExist, PaymentRequest.DoesNotExist) as e:
            messages.error(self.request, "Unable to process payment. Please try again.")
            return redirect('officer_dashboard')

# UPDATE PaymentRequest status
class CancelPaymentRequestView(LoginRequiredMixin, UpdateView):
    model = PaymentRequest
    fields = ['status']
    template_name = 'paymentorg/cancel_request.html'
    
    def get_object(self):
        try:
            student = Student.objects.get(user=self.request.user)
            return PaymentRequest.objects.get(
                request_id=self.kwargs['request_id'], 
                student=student,
                status='PENDING'
            )
        except (Student.DoesNotExist, PaymentRequest.DoesNotExist):
            raise Http404("Payment request not found.")
    
    def form_valid(self, form):
        payment_request = form.save(commit=False)
        payment_request.mark_as_cancelled()
        
        # log activity
        ActivityLog.objects.create(
            user=self.request.user,
            action='PAYMENT_CANCELLED',
            description=f'Student cancelled payment request {payment_request.queue_number}',
            payment_request=payment_request
        )
        
        messages.success(self.request, 'Payment request cancelled successfully.')
        return redirect('student_dashboard')

# mark payment as void with reason (UPDATE Payment status)
class VoidPaymentView(LoginRequiredMixin, UpdateView):
    model = Payment
    fields = ['void_reason']
    template_name = 'paymentorg/void_payment.html'
    
    def get_object(self):
        try:
            officer = Officer.objects.get(user=self.request.user)
            
            if not officer.can_void_payments:
                messages.error(self.request, 'You do not have permission to void payments.')
                return redirect('officer_dashboard')
                
            return Payment.objects.get(
                id=self.kwargs['payment_id'],
                organization=officer.organization,
                status='COMPLETED'
            )
        except (Officer.DoesNotExist, Payment.DoesNotExist):
            raise Http404("Payment not found.")
    
    def form_valid(self, form):
        try:
            officer = Officer.objects.get(user=self.request.user)
            payment = form.save(commit=False)
            
            # update payment status
            payment.mark_as_void(officer, form.cleaned_data['void_reason'])
            
            # log activity
            ActivityLog.objects.create(
                user=self.request.user,
                action='PAYMENT_VOIDED',
                description=f'Officer voided payment OR#{payment.or_number}. Reason: {form.cleaned_data["void_reason"]}',
                payment=payment
            )
            
            messages.success(self.request, f'Payment OR#{payment.or_number} has been voided.')
            return redirect('officer_dashboard')
        except Officer.DoesNotExist:
            messages.error(self.request, "Officer profile not found.")
            return redirect('officer_dashboard')

# edit contact information (UPDATE Student)
class UpdateStudentProfileView(LoginRequiredMixin, UpdateView):
    model = Student
    fields = ['phone_number', 'email']
    template_name = 'paymentorg/update_profile.html'
    success_url = reverse_lazy('student_dashboard')
    
    def get_object(self):
        try:
            return Student.objects.get(user=self.request.user)
        except Student.DoesNotExist:
            raise Http404("Student profile not found.")
    
    def form_valid(self, form):
        # log activity
        ActivityLog.objects.create(
            user=self.request.user,
            action='PROFILE_UPDATED',
            description='Student updated their profile information'
        )
        
        messages.success(self.request, 'Profile updated successfully.')
        return super().form_valid(form)

# delete payment request
class DeletePaymentRequestView(LoginRequiredMixin, DeleteView):
    model = PaymentRequest
    template_name = 'paymentorg/delete_request.html'
    success_url = reverse_lazy('student_dashboard')
    
    def get_object(self):
        try:
            student = Student.objects.get(user=self.request.user)
            return PaymentRequest.objects.get(
                request_id=self.kwargs['request_id'], 
                student=student,
                status='PENDING'
            )
        except (Student.DoesNotExist, PaymentRequest.DoesNotExist):
            raise Http404("Payment request not found.")
    
    def delete(self, request, *args, **kwargs):
        payment_request = self.get_object()
        
        # log activity before deletion
        ActivityLog.objects.create(
            user=request.user,
            action='PAYMENT_REQUEST_DELETED',
            description=f'Student deleted payment request {payment_request.queue_number}',
            payment_request=payment_request
        )
        
        messages.success(request, 'Payment request deleted successfully.')
        return super().delete(request, *args, **kwargs)

 #  return JSON data for student payments status
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
            return JsonResponse({'error': 'Student profile not found'}, status=404)