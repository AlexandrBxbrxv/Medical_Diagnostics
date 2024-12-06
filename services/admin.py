from django.contrib import admin
from services.models import Doctor, Appointment, Service, Analysis, Result


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('id', 'fullname', 'speciality')
    search_fields = ('fullname', 'speciality',)


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'doctor',)
    search_fields = ('title',)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'price', 'appointment',)
    search_fields = ('title',)
    ordering = ('price', 'appointment',)


@admin.register(Analysis)
class AnalysisAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'doctor', 'price',)
    search_fields = ('title',)
    ordering = ('price',)


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'analysis', 'appointment',)
    search_fields = ('title',)
