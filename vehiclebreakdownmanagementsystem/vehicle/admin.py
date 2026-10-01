from django.contrib import admin

from .models import AssistanceRequest, Mechanic

from .models import AssistanceRequest, Mechanic, MechanicSchedule


@admin.register(AssistanceRequest)
class AssistanceRequestAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'customer_name',
        'mobile',
        'vehicle_number',
        'vehicle_type',
        'service',
        'status',
        'created_at',
    )

    list_filter = (
        'status',
        'service',
        'vehicle_type',
    )

    search_fields = (
        'customer_name',
        'mobile',
        'vehicle_number',
    )

    ordering = ('-created_at',)


@admin.register(Mechanic)
class MechanicAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'name',
        'mobile',
        'specialization',
        'location',
        'status',
        'created_at',
    )

    list_filter = (
        'status',
        'specialization',
    )

    search_fields = (
        'name',
        'mobile',
        'specialization',
        'location',
    )

    ordering = ('-created_at',)
# Register your models here.



@admin.register(MechanicSchedule)
class MechanicScheduleAdmin(admin.ModelAdmin):

    list_display = (
        'mechanic',
        'date',
        'start_time',
        'end_time',
        'request',
        'status',
    )

    list_filter = (
        'date',
        'status',
        'mechanic',
    )

    search_fields = (
        'mechanic__name',
        'request__customer_name',
        'request__vehicle_number',
    )

    ordering = (
        'date',
        'start_time',
    )