from django.contrib import admin
from services.models import Doctor, Appointment, Service, Analysis, Result, UsersAppointment


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('id', 'fullname', 'speciality')
    search_fields = ('fullname', 'speciality',)
    ordering = ('id', 'fullname',)


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'doctor',)
    search_fields = ('title',)
    ordering = ('id', 'title',)
    list_filter = ('doctor',)


@admin.register(UsersAppointment)
class UsersAppointmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'title', 'doctor', 'service_id',)
    search_fields = ('title',)
    ordering = ('id', 'title',)
    list_filter = ('doctor', 'owner',)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'price', 'appointment',)
    search_fields = ('title',)
    ordering = ('id', 'title', 'price',)
    list_filter = ('appointment',)


@admin.register(Analysis)
class AnalysisAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'doctor', 'price',)
    search_fields = ('title',)
    ordering = ('id', 'title', 'price',)
    list_filter = ('doctor',)


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'analysis', 'appointment',)
    search_fields = ('title',)
    ordering = ('id', 'title',)
    list_filter = ('analysis', 'appointment',)

