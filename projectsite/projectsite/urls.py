"""
URL configuration for projectsite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from paymentorg import views

urlpatterns = [
    path("admin/", admin.site.urls),
    
    # authentication
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # home and dashboard
    path('', views.HomePageView.as_view(), name='home'),
    path('dashboard/student/', views.StudentDashboardView.as_view(), name='student_dashboard'),
    path('dashboard/officer/', views.OfficerDashboardView.as_view(), name='officer_dashboard'),
    
    # organization
    path('organization/<str:org_code>/fees/', views.OrganizationFeesView.as_view(), name='organization_fees'),
    path('organization/create/', views.CreateOrganizationView.as_view(), name='create_organization'),
    path('organization/<int:pk>/update/', views.UpdateOrganizationView.as_view(), name='update_organization'),
    path('organization/<int:pk>/delete/', views.DeleteOrganizationView.as_view(), name='delete_organization'),

    # feetype
    path('feetype/create/', views.CreateFeeTypeView.as_view(), name='create_feetype'),
    path('feetype/<int:pk>/update/', views.UpdateFeeTypeView.as_view(), name='update_feetype'),
    path('feetype/<int:pk>/delete/', views.DeleteFeeTypeView.as_view(), name='delete_feetype'),

    # officer
    path('officer/create/', views.CreateOfficerView.as_view(), name='create_officer'),
    path('officer/<int:pk>/update/', views.UpdateOfficerView.as_view(), name='update_officer'),
    path('officer/<int:pk>/delete/', views.DeleteOfficerView.as_view(), name='delete_officer'),

    # student
    path('student/create/', views.CreateStudentView.as_view(), name='create_student'),
    path('student/<int:pk>/delete/', views.DeleteStudentView.as_view(), name='delete_student'),
    
    # payment
    path('payment/create/', views.CreatePaymentView.as_view(), name='create_payment'),
    path('payment/<int:pk>/update/', views.UpdatePaymentView.as_view(), name='update_payment'),
    path('payment/<int:pk>/delete/', views.DeletePaymentView.as_view(), name='delete_payment'),
     
    # payment request
    path('payment/generate-qr/', views.GenerateQRPaymentView.as_view(), name='generate_qr'),
    path('payment/process/<uuid:request_id>/', views.ProcessPaymentView.as_view(), name='process_payment'),
    path('payment/cancel/<uuid:request_id>/', views.CancelPaymentRequestView.as_view(), name='cancel_payment_request'),
    path('payment/delete/<uuid:request_id>/', views.DeletePaymentRequestView.as_view(), name='delete_payment_request'),
    
    # payment history and details
    path('payment/history/', views.PaymentHistoryView.as_view(), name='payment_history'),
    path('payment/<int:pk>/', views.PaymentDetailView.as_view(), name='payment_detail'),
    path('payment/search/', views.SearchPaymentsView.as_view(), name='search_payments'),
    
    # payment management
    path('payment/void/<int:payment_id>/', views.VoidPaymentView.as_view(), name='void_payment'),
    
    # profile management
    path('profile/update/', views.UpdateStudentProfileView.as_view(), name='update_profile'),
    
    # api
    path('api/payment-status/', views.PaymentStatusAPIView.as_view(), name='payment_status_api'),
]