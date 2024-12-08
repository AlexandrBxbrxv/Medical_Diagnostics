from django.urls import path

from services.apps import ServicesConfig
from services.views import DoctorCreateView, DoctorListView, DoctorDetailView, DoctorUpdateView, DoctorDeleteView, \
    AppointmentCreateView, AppointmentListView, AppointmentDetailView, AppointmentUpdateView

app_name = ServicesConfig.name


urlpatterns = [
    path('doctor/create/', DoctorCreateView.as_view(), name='doctor_create'),
    path('doctor/list/', DoctorListView.as_view(), name='doctor_list'),
    path('doctor/detail/<int:pk>/', DoctorDetailView.as_view(), name='doctor_detail'),
    path('doctor/update/<int:pk>/', DoctorUpdateView.as_view(), name='doctor_update'),
    path('doctor/delete/<int:pk>/', DoctorDeleteView.as_view(), name='doctor_delete'),

    path('appointment/create/', AppointmentCreateView.as_view(), name='appointment_create'),
    path('appointment/list/', AppointmentListView.as_view(), name='appointment_list'),
    path('appointment/detail/<int:pk>/', AppointmentDetailView.as_view(), name='appointment_detail'),
    path('appointment/update/<int:pk>/', AppointmentUpdateView.as_view(), name='appointment_update'),
]
