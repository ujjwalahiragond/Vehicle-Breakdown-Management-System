from django.db import models
from django.contrib.auth.models import User


# =========================================================
# MECHANIC MODEL
# =========================================================

class Mechanic(models.Model):

    STATUS_CHOICES = [
        ('Available', 'Available'),
        ('Busy', 'Busy'),
        ('Offline', 'Offline'),
    ]

    # Mechanic Login User
    user = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='mechanic_profile'
    )

    name = models.CharField(max_length=100)

    mobile = models.CharField(
        max_length=10
    )

    specialization = models.CharField(
        max_length=100
    )

    location = models.CharField(
        max_length=255
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Available'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.name} - {self.specialization}"


# =========================================================
# ASSISTANCE REQUEST MODEL
# =========================================================

class AssistanceRequest(models.Model):

    # =====================================================
    # REQUEST STATUS
    # =====================================================

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('On The Way', 'On The Way'),
        ('Service Started', 'Service Started'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    # =====================================================
    # SERVICE CHOICES
    # =====================================================

    SERVICE_CHOICES = [
        ('Mechanical Assistance', 'Mechanical Assistance'),
        ('Battery Assistance', 'Battery Assistance'),
        ('Tyre Assistance', 'Tyre Assistance'),
        ('Fuel Assistance', 'Fuel Assistance'),
        ('Towing Service', 'Towing Service'),
        ('Lockout Assistance', 'Lockout Assistance'),
        ('Engine Overheating', 'Engine Overheating'),
        ('Accident Assistance', 'Accident Assistance'),
        ('Fuel Delivery', 'Fuel Delivery'),
        ('Emergency Roadside', 'Emergency Roadside'),
        ('Vehicle Inspection', 'Vehicle Inspection'),
        ('Roadside Support', 'Roadside Support'),
    ]

    # =====================================================
    # CUSTOMER DETAILS
    # =====================================================

    customer_name = models.CharField(
        max_length=100
    )

    mobile = models.CharField(
        max_length=10
    )

    # =====================================================
    # VEHICLE DETAILS
    # =====================================================

    vehicle_number = models.CharField(
        max_length=20
    )

    vehicle_type = models.CharField(
        max_length=50
    )

    # =====================================================
    # SERVICE DETAILS
    # =====================================================

    service = models.CharField(
        max_length=100,
        choices=SERVICE_CHOICES
    )

    problem = models.TextField(
        blank=True
    )

    # =====================================================
    # BREAKDOWN LOCATION
    # =====================================================

    location = models.CharField(
        max_length=255
    )

    # GPS latitude
    latitude = models.DecimalField(
        max_digits=10,
        decimal_places=7,
        null=True,
        blank=True
    )

    # GPS longitude
    longitude = models.DecimalField(
        max_digits=10,
        decimal_places=7,
        null=True,
        blank=True
    )

    # =====================================================
    # ASSIGNED MECHANIC
    # =====================================================

    assigned_mechanic = models.ForeignKey(
        'Mechanic',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='requests'
    )

    # =====================================================
    # REQUEST STATUS
    # =====================================================

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    # =====================================================
    # STATUS DATES
    # =====================================================

    accepted_at = models.DateTimeField(
        null=True,
        blank=True
    )

    on_the_way_at = models.DateTimeField(
        null=True,
        blank=True
    )

    service_started_at = models.DateTimeField(
        null=True,
        blank=True
    )

    completed_at = models.DateTimeField(
        null=True,
        blank=True
    )

    # =====================================================
    # PAYMENT
    # =====================================================

    PAYMENT_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
    ]

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default='Pending'
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    payment_id = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    payment_method = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    payment_date = models.DateTimeField(
        blank=True,
        null=True
    )

    # =====================================================
    # FEEDBACK
    # =====================================================

    rating = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    feedback = models.TextField(
        blank=True
    )

    feedback_date = models.DateTimeField(
        null=True,
        blank=True
    )

    # =====================================================
    # CREATED DATE
    # =====================================================

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    # =====================================================
    # STRING
    # =====================================================

    def __str__(self):
        return f"VBA-{self.id} - {self.customer_name}"
# =========================================================
# MECHANIC SCHEDULE MODEL
# =========================================================

class MechanicSchedule(models.Model):

    STATUS_CHOICES = [
        ('Available', 'Available'),
        ('Busy', 'Busy'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    mechanic = models.ForeignKey(
        Mechanic,
        on_delete=models.CASCADE,
        related_name='schedules'
    )

    request = models.ForeignKey(
        AssistanceRequest,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='schedule'
    )

    date = models.DateField()

    start_time = models.TimeField()

    end_time = models.TimeField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Available'
    )

    notes = models.CharField(
        max_length=255,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ['date', 'start_time']

    def __str__(self):
        return (
            f"{self.mechanic.name} - "
            f"{self.date} - "
            f"{self.start_time}"
        )
class MechanicSalaryPayment(models.Model):

    PAYMENT_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('Cash', 'Cash'),
        ('UPI', 'UPI'),
        ('Bank Transfer', 'Bank Transfer'),
    ]

    mechanic = models.ForeignKey(
        Mechanic,
        on_delete=models.CASCADE,
        related_name='salary_payments'
    )

    month = models.PositiveIntegerField()

    year = models.PositiveIntegerField()

    salary_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default='Pending'
    )

    payment_method = models.CharField(
        max_length=50,
        choices=PAYMENT_METHOD_CHOICES,
        blank=True,
        null=True
    )

    payment_id = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    payment_date = models.DateTimeField(
        blank=True,
        null=True
    )

    notes = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = ('mechanic', 'month', 'year')
        ordering = ['-year', '-month']

    def __str__(self):
        return f"{self.mechanic.name} - {self.month}/{self.year}"                