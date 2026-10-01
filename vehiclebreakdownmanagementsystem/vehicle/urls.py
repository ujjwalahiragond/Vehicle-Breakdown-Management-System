from django.urls import path
from . import views

urlpatterns = [

    # HOME
    path(
        '',
        views.home,
        name='home'
    ),

    # AUTH
    path(
        'register/',
        views.register,
        name='register'
    ),
    path('login/', views.user_login, name='login'),

    path(
        'logout/',
        views.user_logout,
        name='logout'
    ),

    # CUSTOMER DASHBOARD
    path(
        'dashboard/',
        views.user_dashboard,
        name='user_dashboard'
    ),

    # SERVICE
    path(
        'service/<str:service_name>/',
        views.service_detail,
        name='service_detail'
    ),

    # REQUEST
    path(
        'request-assistance/',
        views.request_assistance,
        name='request_assistance'
    ),

    # TRACK
    path(
        'track-request/<int:request_id>/',
        views.track_request,
        name='track_request'
    ),

    # ADMIN
    path(
        'admin-dashboard/',
        views.admin_dashboard,
        name='admin_dashboard'
    ),

    path(
        'manage-request/<int:request_id>/',
        views.manage_request,
        name='manage_request'
    ),

    path(
        'delete-request/<int:request_id>/',
        views.delete_request,
        name='delete_request'
    ),

    # PAYMENT
    path(
        'payment/<int:request_id>/',
        views.payment,
        name='payment'
    ),

    # PDF RECEIPT
    path(
        'payment-receipt/<int:request_id>/',
        views.payment_receipt_pdf,
        name='payment_receipt_pdf'
    ),

    # MECHANIC
    path(
        'mechanic-schedule/',
        views.mechanic_schedule,
        name='mechanic_schedule'
    ),

    path(
        'mechanic-monthly-payment/',
        views.mechanic_monthly_payment,
        name='mechanic_monthly_payment'
    ),

    path(
        'admin-requests/',
        views.admin_requests,
        name='admin_requests'
    ),

    path(
        'mechanic-salary-payment/<int:mechanic_id>/',
        views.mechanic_salary_payment,
        name='mechanic_salary_payment'
    ),

    path(
        'mechanic-salary-receipt/<int:payment_id>/',
        views.mechanic_salary_receipt_pdf,
        name='mechanic_salary_receipt_pdf'
    ),
    path(
    'delete-mechanic-salary-payment/<int:payment_id>/',
    views.delete_mechanic_salary_payment,
    name='delete_mechanic_salary_payment'
),
]