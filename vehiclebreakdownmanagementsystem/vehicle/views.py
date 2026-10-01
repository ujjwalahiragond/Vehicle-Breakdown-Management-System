from datetime import datetime, timedelta

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse
from django.utils import timezone

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

from .models import (
    AssistanceRequest,
    Mechanic,
    MechanicSchedule,
    MechanicSalaryPayment
)

SERVICE_AMOUNTS = {
    "Mechanical Assistance": 500,
    "Battery Assistance": 300,
    "Tyre Assistance": 400,
    "Fuel Assistance": 250,
    "Towing Service": 1000,
    "Lockout Assistance": 350,
    "Engine Overheating": 600,
    "Accident Assistance": 1500,
    "Fuel Delivery": 300,
    "Emergency Roadside": 500,
    "Vehicle Inspection": 400,
    "Roadside Support": 350,
}

SERVICE_MECHANICS = {
    "Mechanical Assistance": "Mechanical & Engine",
    "Battery Assistance": "Battery & Electrical",
    "Tyre Assistance": "Tyre & Wheel",
    "Fuel Assistance": "Fuel & Roadside Assistance",
    "Towing Service": "Towing & Recovery",
    "Lockout Assistance": "Vehicle Lockout",
    "Engine Overheating": "Engine & Cooling",
    "Accident Assistance": "Accident & Emergency",
    "Fuel Delivery": "Fuel & Roadside Assistance",
    "Emergency Roadside": "Accident & Emergency",
    "Vehicle Inspection": "Mechanical & Engine",
    "Roadside Support": "Fuel & Roadside Assistance",
}

SERVICE_DURATION_MINUTES = {
    "Mechanical Assistance": 60,
    "Battery Assistance": 30,
    "Tyre Assistance": 40,
    "Fuel Assistance": 40,
    "Towing Service": 90,
    "Lockout Assistance": 30,
    "Engine Overheating": 60,
    "Accident Assistance": 90,
    "Fuel Delivery": 40,
    "Emergency Roadside": 60,
    "Vehicle Inspection": 45,
    "Roadside Support": 60,
}


def get_next_available_slot(mechanic, start_datetime, duration_minutes):
    duration = timedelta(minutes=duration_minutes)

    candidate_start = start_datetime.replace(
        second=0,
        microsecond=0
    )

    minutes = candidate_start.minute
    remainder = minutes % 15

    if remainder != 0:
        candidate_start += timedelta(
            minutes=15 - remainder
        )

    schedules = MechanicSchedule.objects.filter(
        mechanic=mechanic
    ).order_by(
        'date',
        'start_time'
    )

    for schedule in schedules:

        if schedule.status == 'Cancelled':
            continue

        schedule_start = timezone.make_aware(
            datetime.combine(
                schedule.date,
                schedule.start_time
            )
        )

        schedule_end = timezone.make_aware(
            datetime.combine(
                schedule.date,
                schedule.end_time
            )
        )

        if schedule_end <= candidate_start:
            continue

        if candidate_start.date() < schedule.date:
            return (
                candidate_start,
                candidate_start + duration
            )

        if candidate_start.date() == schedule.date:

            candidate_end = candidate_start + duration

            if candidate_end <= schedule_start:
                return (
                    candidate_start,
                    candidate_end
                )

            if candidate_start < schedule_end:
                candidate_start = schedule_end

    return (
        candidate_start,
        candidate_start + duration
    )


@login_required
def home(request):
    return render(
        request,
        'vehicle/index.html'
    )


def register(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get(
            'confirm_password'
        )

        if password != confirm_password:
            messages.error(
                request,
                "Passwords do not match."
            )
            return redirect('register')

        if User.objects.filter(
            username=username
        ).exists():

            messages.error(
                request,
                "Username already exists."
            )
            return redirect('register')

        User.objects.create_user(
            username=username,
            password=password
        )

        messages.success(
            request,
            "Registration successful. Please login."
        )

        return redirect('login')

    return render(
        request,
        'vehicle/register.html'
    )


def user_login(request):

    if request.method == 'POST':

        username = request.POST.get(
            'username',
            ''
        ).strip()

        password = request.POST.get(
            'password',
            ''
        )

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(
                request,
                user
            )

            if user.is_superuser:
                return redirect(
                    'admin_dashboard'
                )

            return redirect('home')

        messages.error(
            request,
            "Invalid username or password."
        )

    return render(
        request,
        'vehicle/login.html'
    )


def user_logout(request):
    logout(request)
    return redirect('login')


@login_required
def user_dashboard(request):

    requests = AssistanceRequest.objects.filter(
        customer_name=request.user.username
    ).select_related(
        'assigned_mechanic'
    ).order_by(
        '-created_at'
    )

    return render(
        request,
        'vehicle/user_dashboard.html',
        {
            'requests': requests
        }
    )


def service_detail(request, service_name):

    SERVICE_DETAILS = {

        "Mechanical Assistance": {
            "time": "30 - 60 Minutes",
            "need": [
                "Engine problem",
                "Vehicle breakdown",
                "Vehicle starting problem",
                "Unusual engine noise"
            ],
            "provide": [
                "Engine inspection",
                "Basic mechanical repair",
                "Breakdown diagnosis",
                "On-road mechanical support"
            ]
        },

        "Battery Assistance": {
            "time": "15 - 30 Minutes",
            "need": [
                "Dead battery",
                "Vehicle not starting",
                "Weak battery",
                "Battery connection problem"
            ],
            "provide": [
                "Battery inspection",
                "Battery jump start",
                "Battery connection check",
                "Battery replacement support"
            ]
        },

        "Tyre Assistance": {
            "time": "20 - 40 Minutes",
            "need": [
                "Flat tyre",
                "Puncture",
                "Tyre damage",
                "Tyre replacement"
            ],
            "provide": [
                "Tyre inspection",
                "Puncture assistance",
                "Spare tyre installation",
                "Tyre replacement support"
            ]
        },

        "Fuel Assistance": {
            "time": "20 - 40 Minutes",
            "need": [
                "Vehicle stopped due to fuel problem",
                "Fuel system problem",
                "Emergency roadside fuel support"
            ],
            "provide": [
                "Fuel system inspection",
                "Roadside assistance",
                "Emergency support",
                "Fuel-related troubleshooting"
            ]
        },

        "Towing Service": {
            "time": "30 - 90 Minutes",
            "need": [
                "Vehicle cannot move",
                "Major vehicle breakdown",
                "Accident vehicle",
                "Engine failure"
            ],
            "provide": [
                "Vehicle towing",
                "Safe vehicle recovery",
                "Breakdown recovery",
                "Workshop transportation"
            ]
        },

        "Lockout Assistance": {
            "time": "15 - 30 Minutes",
            "need": [
                "Keys locked inside vehicle",
                "Lost vehicle keys",
                "Vehicle lock problem"
            ],
            "provide": [
                "Vehicle lockout assistance",
                "Safe access support",
                "Emergency roadside support"
            ]
        },

        "Engine Overheating": {
            "time": "30 - 60 Minutes",
            "need": [
                "Engine overheating",
                "Temperature warning",
                "Coolant problem",
                "Vehicle stopping due to heat"
            ],
            "provide": [
                "Cooling system inspection",
                "Coolant level check",
                "Engine temperature inspection",
                "Roadside troubleshooting"
            ]
        },

        "Accident Assistance": {
            "time": "30 - 90 Minutes",
            "need": [
                "Road accident",
                "Vehicle damage",
                "Emergency roadside situation"
            ],
            "provide": [
                "Emergency roadside assistance",
                "Vehicle inspection",
                "Towing coordination",
                "Recovery support"
            ]
        },

        "Fuel Delivery": {
            "time": "20 - 40 Minutes",
            "need": [
                "Vehicle out of fuel",
                "Emergency fuel requirement",
                "Vehicle stopped on road"
            ],
            "provide": [
                "Emergency fuel delivery",
                "Roadside assistance",
                "Vehicle restart support"
            ]
        },

        "Emergency Roadside": {
            "time": "20 - 60 Minutes",
            "need": [
                "Unexpected vehicle breakdown",
                "Roadside emergency",
                "Vehicle stopped suddenly"
            ],
            "provide": [
                "Emergency roadside support",
                "Initial vehicle inspection",
                "Breakdown assistance",
                "Mechanic support"
            ]
        },

        "Vehicle Inspection": {
            "time": "30 - 45 Minutes",
            "need": [
                "Vehicle performance problem",
                "Warning signs",
                "Unusual noise",
                "Pre-trip inspection"
            ],
            "provide": [
                "Basic vehicle inspection",
                "Problem identification",
                "Mechanical check",
                "Safety inspection"
            ]
        },

        "Roadside Support": {
            "time": "20 - 60 Minutes",
            "need": [
                "Minor roadside problem",
                "Vehicle breakdown",
                "Emergency vehicle support"
            ],
            "provide": [
                "Basic roadside assistance",
                "Vehicle inspection",
                "Minor troubleshooting",
                "Mechanic support"
            ]
        }
    }

    amount = SERVICE_AMOUNTS.get(
        service_name,
        0
    )

    details = SERVICE_DETAILS.get(
        service_name,
        {
            "time": "30 - 60 Minutes",
            "need": [
                "Vehicle breakdown",
                "Roadside emergency"
            ],
            "provide": [
                "Roadside assistance",
                "Vehicle inspection",
                "Mechanic support"
            ]
        }
    )

    mechanic_specialization = SERVICE_MECHANICS.get(
        service_name,
        ""
    )

    service_mechanics = Mechanic.objects.filter(
        specialization=mechanic_specialization
    ).order_by(
        "name"
    )

    return render(
        request,
        'vehicle/service_detail.html',
        {
            'service_name': service_name,
            'amount': amount,
            'estimated_time': details['time'],
            'when_needed': details['need'],
            'what_provide': details['provide'],
            'service_mechanics': service_mechanics,
            'mechanic_specialization': mechanic_specialization,
        }
    )


@login_required
def admin_dashboard(request):

    requests = AssistanceRequest.objects.select_related(
        'assigned_mechanic'
    ).order_by(
        '-created_at'
    )

    recent_requests = requests[:10]

    total_requests = requests.count()

    pending_requests = AssistanceRequest.objects.filter(
        status='Pending'
    ).count()

    accepted_requests = AssistanceRequest.objects.filter(
        status='Accepted'
    ).count()

    on_the_way_requests = AssistanceRequest.objects.filter(
        status='On The Way'
    ).count()

    service_started_requests = AssistanceRequest.objects.filter(
        status='Service Started'
    ).count()

    completed_requests = AssistanceRequest.objects.filter(
        status='Completed'
    ).count()

    cancelled_requests = AssistanceRequest.objects.filter(
        status='Cancelled'
    ).count()

    mechanics = Mechanic.objects.all().order_by(
        'name'
    )

    total_mechanics = mechanics.count()

    available_mechanics = Mechanic.objects.filter(
        status='Available'
    ).count()

    paid_requests = AssistanceRequest.objects.filter(
        payment_status='Paid'
    ).count()

    unpaid_requests = AssistanceRequest.objects.filter(
        payment_status='Pending'
    ).count()

    total_paid_revenue = 0

    paid_items = AssistanceRequest.objects.filter(
        payment_status='Paid'
    )

    for item in paid_items:

        if item.amount:
            total_paid_revenue += item.amount

    pending_payment = 0

    pending_items = AssistanceRequest.objects.filter(
        payment_status='Pending'
    )

    for item in pending_items:

        if item.amount:
            pending_payment += item.amount

    return render(
        request,
        'vehicle/admin_dashboard.html',
        {
            'requests': requests,
            'recent_requests': recent_requests,
            'total_requests': total_requests,
            'pending_requests': pending_requests,
            'accepted_requests': accepted_requests,
            'on_the_way_requests': on_the_way_requests,
            'service_started_requests': service_started_requests,
            'completed_requests': completed_requests,
            'cancelled_requests': cancelled_requests,
            'mechanics': mechanics,
            'total_mechanics': total_mechanics,
            'available_mechanics': available_mechanics,
            'total_paid_revenue': total_paid_revenue,
            'pending_payment': pending_payment,
            'paid_requests': paid_requests,
            'unpaid_requests': unpaid_requests,
        }
    )


@login_required
def request_assistance(request):

    if request.method == "POST":

        # =================================================
        # CUSTOMER DETAILS
        # =================================================

        customer_name = request.user.username

        mobile = request.POST.get(
            "mobile",
            ""
        ).strip()

        vehicle_number = request.POST.get(
            "vehicle_number",
            ""
        ).strip()

        vehicle_type = request.POST.get(
            "vehicle_type",
            ""
        ).strip()

        service = request.POST.get(
            "service",
            ""
        ).strip()

        location = request.POST.get(
            "location",
            ""
        ).strip()

        problem = request.POST.get(
            "problem",
            ""
        ).strip()


        # =================================================
        # SERVICE AMOUNT
        # =================================================

        amount = SERVICE_AMOUNTS.get(
            service,
            0
        )


        # =================================================
        # CREATE REQUEST
        # =================================================

        assistance_request = AssistanceRequest.objects.create(

            customer_name=customer_name,

            mobile=mobile,

            vehicle_number=vehicle_number.upper(),

            vehicle_type=vehicle_type,

            service=service,

            location=location,

            problem=problem,

            amount=amount,

            status="Pending",

            payment_status="Pending",
        )


        # =================================================
        # FIND MATCHING MECHANICS
        # =================================================

        specialization = SERVICE_MECHANICS.get(
            service,
            ""
        )

        matching_mechanics = Mechanic.objects.filter(
            specialization=specialization
        ).order_by(
            'name'
        )


        # =================================================
        # SERVICE DURATION
        # =================================================

        duration_minutes = SERVICE_DURATION_MINUTES.get(
            service,
            60
        )


        # =================================================
        # CURRENT DATE & TIME
        # =================================================

        current_datetime = timezone.localtime(
            timezone.now()
        )


        # =================================================
        # FIND NEXT AVAILABLE SLOT
        # =================================================

        selected_mechanic = None

        selected_start = None

        selected_end = None


        for mechanic in matching_mechanics:

            start_time, end_time = get_next_available_slot(

                mechanic,

                current_datetime,

                duration_minutes
            )


            # ---------------------------------------------
            # IMPORTANT:
            # Never allow a slot before current time
            # ---------------------------------------------

            if start_time < current_datetime:

                start_time = current_datetime.replace(
                    second=0,
                    microsecond=0
                )

                minutes = start_time.minute

                remainder = minutes % 15

                if remainder != 0:

                    start_time += timedelta(
                        minutes=15 - remainder
                    )

                end_time = (
                    start_time
                    + timedelta(
                        minutes=duration_minutes
                    )
                )


            # ---------------------------------------------
            # Select earliest available mechanic
            # ---------------------------------------------

            if (
                selected_start is None
                or start_time < selected_start
            ):

                selected_mechanic = mechanic

                selected_start = start_time

                selected_end = end_time


        # =================================================
        # ASSIGN MECHANIC + CREATE SCHEDULE
        # =================================================

        if selected_mechanic:

            assistance_request.assigned_mechanic = (
                selected_mechanic
            )

            assistance_request.save(
                update_fields=[
                    'assigned_mechanic'
                ]
            )


            # ---------------------------------------------
            # Determine schedule status
            # ---------------------------------------------

            if (
                selected_start.date()
                == current_datetime.date()
                and selected_start <= current_datetime
                < selected_end
            ):

                schedule_status = 'Busy'

            else:

                schedule_status = 'Available'


            # ---------------------------------------------
            # Create schedule
            # ---------------------------------------------

            MechanicSchedule.objects.create(

                mechanic=selected_mechanic,

                request=assistance_request,

                date=selected_start.date(),

                start_time=selected_start.time(),

                end_time=selected_end.time(),

                status=schedule_status,

                notes=(
                    f"{service} - "
                    f"{customer_name} - "
                    f"{vehicle_number.upper()}"
                )
            )


            # ---------------------------------------------
            # Mechanic status
            # ---------------------------------------------

            if schedule_status == 'Busy':

                selected_mechanic.status = 'Busy'

            else:

                selected_mechanic.status = 'Available'


            selected_mechanic.save(
                update_fields=[
                    'status'
                ]
            )


        # =================================================
        # GO TO TRACK REQUEST
        # =================================================

        return redirect(
            "track_request",
            request_id=assistance_request.id
        )


    # =====================================================
    # GET REQUEST PAGE
    # =====================================================

    service_selected = request.GET.get(
        "service",
        ""
    )


    return render(
        request,
        "vehicle/request_assistance.html",
        {
            "service_selected": service_selected,

            "selected_service": service_selected,

            "service_amount": SERVICE_AMOUNTS.get(
                service_selected,
                0
            ),
        }
    )
@login_required
def track_request(request, request_id):

    assistance_request = get_object_or_404(
        AssistanceRequest,
        id=request_id,
        customer_name=request.user.username
    )

    status_steps = [
        "Pending",
        "Accepted",
        "On The Way",
        "Service Started",
        "Completed",
    ]

    current_status = assistance_request.status

    timeline = []

    if current_status == "Cancelled":

        for status in status_steps:

            timeline.append({
                "name": status,
                "state": "cancelled"
            })

    else:

        if current_status in status_steps:
            current_index = status_steps.index(
                current_status
            )
        else:
            current_index = 0

        for index, status in enumerate(
            status_steps
        ):

            if index < current_index:
                state = "completed"

            elif index == current_index:
                state = "current"

            else:
                state = "pending"

            timeline.append({
                "name": status,
                "state": state
            })

    return render(
        request,
        "vehicle/track_request.html",
        {
            "request": assistance_request,
            "selected_request": assistance_request,
            "timeline": timeline,
            "current_status": current_status,
        }
    )


@login_required
def manage_request(request, request_id):

    assistance_request = get_object_or_404(
        AssistanceRequest,
        id=request_id
    )

    mechanics = Mechanic.objects.all().order_by(
        'name'
    )

    if request.method == 'POST':

        status = request.POST.get(
            'status',
            ''
        ).strip()

        mechanic_id = request.POST.get(
            'mechanic',
            ''
        ).strip()

        if status:
            assistance_request.status = status

        if mechanic_id:

            mechanic = get_object_or_404(
                Mechanic,
                id=mechanic_id
            )

            assistance_request.assigned_mechanic = mechanic

        else:

            assistance_request.assigned_mechanic = None

        current_time = timezone.now()

        if status == 'Accepted':
            assistance_request.accepted_at = current_time

        elif status == 'On The Way':
            assistance_request.on_the_way_at = current_time

        elif status == 'Service Started':
            assistance_request.service_started_at = current_time

        elif status == 'Completed':
            assistance_request.completed_at = current_time

        assistance_request.save()

        if mechanic_id:

            mechanic = assistance_request.assigned_mechanic

            schedule = MechanicSchedule.objects.filter(
                request=assistance_request
            ).first()

            if schedule:

                schedule.mechanic = mechanic

                if status == 'Completed':
                    schedule.status = 'Completed'

                elif status == 'Cancelled':
                    schedule.status = 'Cancelled'

                else:
                    schedule.status = 'Busy'

                schedule.notes = (
                    f"{assistance_request.service} - "
                    f"{assistance_request.customer_name} - "
                    f"{assistance_request.vehicle_number}"
                )

                schedule.save()

            else:

                start_datetime = timezone.localtime(
                    timezone.now()
                )

                duration_minutes = SERVICE_DURATION_MINUTES.get(
                    assistance_request.service,
                    60
                )

                start_time, end_time = get_next_available_slot(
                    mechanic,
                    start_datetime,
                    duration_minutes
                )

                MechanicSchedule.objects.create(
                    mechanic=mechanic,
                    request=assistance_request,
                    date=start_time.date(),
                    start_time=start_time.time(),
                    end_time=end_time.time(),
                    status='Busy',
                    notes=(
                        f"{assistance_request.service} - "
                        f"{assistance_request.customer_name} - "
                        f"{assistance_request.vehicle_number}"
                    )
                )

            if status == 'Completed':
                mechanic.status = 'Available'

            elif status == 'Cancelled':
                mechanic.status = 'Available'

            else:
                mechanic.status = 'Busy'

            mechanic.save(
                update_fields=[
                    'status'
                ]
            )

        messages.success(
            request,
            "Request updated and mechanic schedule created successfully."
        )

        return redirect(
            'admin_dashboard'
        )

    return render(
        request,
        'vehicle/manage_request.html',
        {
            'assistance': assistance_request,
            'assistance_request': assistance_request,
            'mechanics': mechanics,
        }
    )


@login_required
def delete_request(request, request_id):

    assistance_request = get_object_or_404(
        AssistanceRequest,
        id=request_id
    )

    assistance_request.delete()

    messages.success(
        request,
        "Request deleted successfully."
    )

    return redirect(
        'admin_dashboard'
    )


@login_required
def payment(request, request_id):

    assistance_request = get_object_or_404(
        AssistanceRequest,
        id=request_id,
        customer_name=request.user.username
    )

    if assistance_request.payment_status == 'Paid':

        return redirect(
            'track_request',
            request_id=assistance_request.id
        )

    if request.method == 'POST':

        payment_method = request.POST.get(
            'payment_method',
            ''
        ).strip()

        if not payment_method:

            messages.error(
                request,
                "Please select a payment method."
            )

            return redirect(
                'payment',
                request_id=assistance_request.id
            )

        assistance_request.payment_status = 'Paid'

        assistance_request.payment_method = payment_method

        assistance_request.payment_id = (
            f"PAY-{assistance_request.id}"
        )

        assistance_request.payment_date = timezone.now()

        assistance_request.save()

        messages.success(
            request,
            "Payment completed successfully."
        )

        return redirect(
            'track_request',
            request_id=assistance_request.id
        )

    return render(
        request,
        'vehicle/payment.html',
        {
            'request_data': assistance_request,
            'assistance_request': assistance_request,
            'payment_request': assistance_request,
            'request': assistance_request,
        }
    )


# =========================================================
# CUSTOMER / ADMIN PAYMENT RECEIPT PDF
# =========================================================

@login_required
def payment_receipt_pdf(request, request_id):

    # ONLY CHANGE:
    # Admin/Superuser can open any receipt.
    # Customer can open only their own receipt.

    if request.user.is_superuser:

        assistance_request = get_object_or_404(
            AssistanceRequest,
            id=request_id
        )

    else:

        assistance_request = get_object_or_404(
            AssistanceRequest,
            id=request_id,
            customer_name=request.user.username
        )

    if assistance_request.payment_status != 'Paid':

        if request.user.is_superuser:

            messages.error(
                request,
                "Payment has not been completed for this request."
            )

            return redirect(
                'admin_dashboard'
            )

        return redirect(
            'payment',
            request_id=assistance_request.id
        )

    response = HttpResponse(
        content_type='application/pdf'
    )

    response['Content-Disposition'] = (
        f'attachment; '
        f'filename="Receipt_VBA-{assistance_request.id}.pdf"'
    )

    pdf = canvas.Canvas(
        response,
        pagesize=A4
    )

    width, height = A4

    pdf.setFont(
        "Helvetica-Bold",
        20
    )

    pdf.drawCentredString(
        width / 2,
        height - 60,
        "M K GARAGE, JATH"
    )

    pdf.setFont(
        "Helvetica-Bold",
        15
    )

    pdf.drawCentredString(
        width / 2,
        height - 88,
        "PAYMENT RECEIPT"
    )

    pdf.line(
        50,
        height - 110,
        width - 50,
        height - 110
    )

    y = height - 150

    details = [

        (
            "Request ID",
            f"VBA-{assistance_request.id}"
        ),

        (
            "Customer Name",
            assistance_request.customer_name
        ),

        (
            "Mobile",
            assistance_request.mobile
        ),

        (
            "Vehicle Number",
            assistance_request.vehicle_number
        ),

        (
            "Vehicle Type",
            assistance_request.vehicle_type
        ),

        (
            "Service",
            assistance_request.service
        ),

        (
            "Location",
            assistance_request.location
        ),

        (
            "Problem",
            assistance_request.problem
        ),

        (
            "Amount",
            f"Rs. {assistance_request.amount}"
        ),

        (
            "Payment Status",
            assistance_request.payment_status
        ),

        (
            "Payment Method",
            assistance_request.payment_method or "-"
        ),

        (
            "Payment ID",
            assistance_request.payment_id or "-"
        ),

        (
            "Payment Date",
            assistance_request.payment_date.strftime(
                "%d-%m-%Y %I:%M %p"
            )
            if assistance_request.payment_date
            else "-"
        ),
    ]

    for label, value in details:

        pdf.setFont(
            "Helvetica-Bold",
            11
        )

        pdf.drawString(
            70,
            y,
            label + ":"
        )

        pdf.setFont(
            "Helvetica",
            11
        )

        pdf.drawString(
            230,
            y,
            str(value)
        )

        y -= 26

    pdf.line(
        50,
        100,
        width - 50,
        100
    )

    pdf.setFont(
        "Helvetica-Bold",
        12
    )

    pdf.drawCentredString(
        width / 2,
        78,
        "Payment Received Successfully"
    )

    pdf.setFont(
        "Helvetica",
        9
    )

    pdf.drawCentredString(
        width / 2,
        58,
        "This is a computer generated receipt."
    )

    pdf.drawCentredString(
        width / 2,
        43,
        "M K GARAGE, JATH"
    )

    pdf.save()

    return response

@login_required
def mechanic_schedule(request):

    schedules = list(
        MechanicSchedule.objects.select_related(
            'mechanic',
            'request'
        ).order_by(
            'date',
            'start_time',
            'mechanic__name'
        )
    )

    now = timezone.localtime(timezone.now())

    busy_mechanics = set()
    upcoming_count = 0
    completed_count = 0

    for item in schedules:

        # -------------------------------------------------
        # NO REQUEST
        # -------------------------------------------------

        if not item.request:

            if item.status == 'Cancelled':

                item.live_status = 'Cancelled'

            elif item.status == 'Completed':

                item.live_status = 'Completed'
                completed_count += 1

            else:

                item.live_status = 'Upcoming'
                upcoming_count += 1

            continue


        # -------------------------------------------------
        # REQUEST BASED STATUS
        # -------------------------------------------------

        request_status = item.request.status


        # -------------------------------------------------
        # CANCELLED
        # -------------------------------------------------

        if request_status == 'Cancelled' or item.status == 'Cancelled':

            item.live_status = 'Cancelled'


        # -------------------------------------------------
        # COMPLETED
        # -------------------------------------------------

        elif request_status == 'Completed':

            item.live_status = 'Completed'
            completed_count += 1


        # -------------------------------------------------
        # SERVICE STARTED
        # -------------------------------------------------

        elif request_status == 'Service Started':

            item.live_status = 'Busy'

            busy_mechanics.add(
                item.mechanic.id
            )


        # -------------------------------------------------
        # FUTURE / ACTIVE REQUEST
        # -------------------------------------------------

        else:

            item.live_status = 'Upcoming'
            upcoming_count += 1


    # -----------------------------------------------------
    # MECHANIC COUNTS
    # -----------------------------------------------------

    total_mechanics = Mechanic.objects.count()

    busy_count = len(busy_mechanics)

    available_count = max(
        total_mechanics - busy_count,
        0
    )


    # -----------------------------------------------------
    # PAGE
    # -----------------------------------------------------

    return render(
        request,
        'vehicle/mechanic_schedule.html',
        {
            'schedules': schedules,

            'total_mechanics': total_mechanics,

            'available_count': available_count,

            'busy_count': busy_count,

            'upcoming_count': upcoming_count,

            'completed_count': completed_count,

            'current_date': now.date(),

            'current_time': now.time(),
        }
    )
@login_required
def mechanic_monthly_payment(request):

    mechanics = Mechanic.objects.all().order_by(
        'name'
    )

    payments = MechanicSalaryPayment.objects.select_related(
        'mechanic'
    ).order_by(
        '-year',
        '-month',
        'mechanic__name'
    )

    return render(
        request,
        'vehicle/mechanic_monthly_payment.html',
        {
            'mechanics': mechanics,
            'payments': payments
        }
    )


@login_required
def admin_requests(request):

    requests = AssistanceRequest.objects.select_related(
        'assigned_mechanic'
    ).order_by(
        '-created_at'
    )

    return render(
        request,
        'vehicle/admin_requests.html',
        {
            'requests': requests
        }
    )


@login_required
def mechanic_salary_payment(
    request,
    mechanic_id
):

    mechanic = get_object_or_404(
        Mechanic,
        id=mechanic_id
    )

    if request.method == 'POST':

        month = request.POST.get(
            'month'
        )

        year = request.POST.get(
            'year'
        )

        salary_amount = request.POST.get(
            'salary_amount'
        )

        payment_method = request.POST.get(
            'payment_method'
        )

        payment_id = request.POST.get(
            'payment_id'
        )

        notes = request.POST.get(
            'notes'
        )

        MechanicSalaryPayment.objects.update_or_create(
            mechanic=mechanic,
            month=month,
            year=year,
            defaults={
                'salary_amount': salary_amount,
                'payment_status': 'Paid',
                'payment_method': payment_method,
                'payment_id': payment_id,
                'payment_date': timezone.now(),
                'notes': notes,
            }
        )

        messages.success(
            request,
            "Mechanic salary payment saved successfully."
        )

        return redirect(
            'mechanic_monthly_payment'
        )

    return render(
        request,
        'vehicle/mechanic_salary_payment.html',
        {
            'mechanic': mechanic
        }
    )


@login_required
def mechanic_salary_receipt_pdf(
    request,
    payment_id
):

    payment = get_object_or_404(
        MechanicSalaryPayment,
        id=payment_id
    )

    response = HttpResponse(
        content_type='application/pdf'
    )

    response['Content-Disposition'] = (
        f'inline; '
        f'filename="Salary_Receipt_{payment.id}.pdf"'
    )

    pdf = canvas.Canvas(
        response,
        pagesize=A4
    )

    width, height = A4

    pdf.setFont(
        "Helvetica-Bold",
        20
    )

    pdf.drawCentredString(
        width / 2,
        height - 60,
        "M K GARAGE, JATH"
    )

    pdf.setFont(
        "Helvetica-Bold",
        14
    )

    pdf.drawCentredString(
        width / 2,
        height - 85,
        "MECHANIC SALARY PAYMENT RECEIPT"
    )

    pdf.line(
        50,
        height - 105,
        width - 50,
        height - 105
    )

    y = height - 145

    details = [

        (
            "Receipt ID",
            f"SR-{payment.id}"
        ),

        (
            "Mechanic Name",
            payment.mechanic.name
        ),

        (
            "Specialization",
            payment.mechanic.specialization
        ),

        (
            "Mobile",
            payment.mechanic.mobile
        ),

        (
            "Location",
            payment.mechanic.location
        ),

        (
            "Salary Month",
            str(payment.month)
        ),

        (
            "Salary Year",
            str(payment.year)
        ),

        (
            "Salary Amount",
            f"Rs. {payment.salary_amount}"
        ),

        (
            "Payment Status",
            payment.payment_status
        ),

        (
            "Payment Method",
            payment.payment_method or "-"
        ),

        (
            "Payment ID",
            payment.payment_id or "-"
        ),

        (
            "Payment Date",
            payment.payment_date.strftime(
                "%d-%m-%Y %H:%M"
            )
            if payment.payment_date
            else "-"
        ),
    ]

    for label, value in details:

        pdf.setFont(
            "Helvetica-Bold",
            11
        )

        pdf.drawString(
            70,
            y,
            label + ":"
        )

        pdf.setFont(
            "Helvetica",
            11
        )

        pdf.drawString(
            230,
            y,
            str(value)
        )

        y -= 27

    pdf.setFont(
        "Helvetica-Bold",
        11
    )

    pdf.drawString(
        70,
        y,
        "Notes:"
    )

    pdf.setFont(
        "Helvetica",
        11
    )

    notes = payment.notes or "-"

    pdf.drawString(
        230,
        y,
        notes[:70]
    )

    pdf.line(
        50,
        100,
        width - 50,
        100
    )

    pdf.setFont(
        "Helvetica",
        10
    )

    pdf.drawCentredString(
        width / 2,
        75,
        "This is a computer generated payment receipt."
    )

    pdf.drawCentredString(
        width / 2,
        55,
        "M K GARAGE, JATH"
    )

    pdf.save()

    return response


@login_required
def delete_mechanic_salary_payment(
    request,
    payment_id
):

    if request.method == "POST":

        payment = get_object_or_404(
            MechanicSalaryPayment,
            id=payment_id
        )

        payment.delete()

        messages.success(
            request,
            "Mechanic salary payment deleted successfully."
        )

    return redirect(
        'mechanic_monthly_payment'
    )