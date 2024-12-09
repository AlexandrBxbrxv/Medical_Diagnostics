from django.urls import path

from services.apps import ServicesConfig
from services.views import DoctorCreateView, DoctorListView, DoctorDetailView, DoctorUpdateView, DoctorDeleteView

app_name = ServicesConfig.name


urlpatterns = [
    path('doctor/create/', DoctorCreateView.as_view(), name='doctor_create'),
    path('doctor/list/', DoctorListView.as_view(), name='doctor_list'),
    path('doctor/detail/<int:pk>/', DoctorDetailView.as_view(), name='doctor_detail'),
    path('doctor/update/<int:pk>/', DoctorUpdateView.as_view(), name='doctor_update'),
    path('doctor/delete/<int:pk>/', DoctorDeleteView.as_view(), name='doctor_delete'),
]
