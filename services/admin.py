from django.contrib import admin
from services.models import Doctor, Appointment, Analysis, Result


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('id', 'fullname', 'speciality')
    search_fields = ('fullname', 'speciality',)


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'doctor', 'price',)
    search_fields = ('title',)
    ordering = ('price',)


@admin.register(Analysis)
class AnalysisAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'doctor', 'price',)
    search_fields = ('title',)
    ordering = ('price',)


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'analysis', 'appointment',)
    search_fields = ('title',)
