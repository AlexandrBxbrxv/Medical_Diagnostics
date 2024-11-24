from django.urls import path

from services.apps import ServicesConfig
from services.views import DoctorCreateView

app_name = ServicesConfig.name


urlpatterns = [
    path('doctor/create/', DoctorCreateView.as_view(), name='doctor_create')
]
