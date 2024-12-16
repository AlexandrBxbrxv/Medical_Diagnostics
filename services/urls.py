from django.urls import path

from services.apps import ServicesConfig
from services.views import DoctorCreateView, DoctorListView, DoctorDetailView, DoctorUpdateView, DoctorDeleteView, \
    AppointmentCreateView, AppointmentListView, AppointmentDetailView, AppointmentUpdateView, AppointmentDeleteView, \
    AnalysisCreateView, AnalysisListView, AnalysisDetailView, AnalysisUpdateView, AnalysisDeleteView

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
    path('appointment/delete/<int:pk>/', AppointmentDeleteView.as_view(), name='appointment_delete'),

    path('analysis/create/', AnalysisCreateView.as_view(), name='analysis_create'),
    path('analysis/list/', AnalysisListView.as_view(), name='analysis_list'),
    path('analysis/detail/<int:pk>/', AnalysisDetailView.as_view(), name='analysis_detail'),
    path('analysis/update/<int:pk>/', AnalysisUpdateView.as_view(), name='analysis_update'),
    path('analysis/delete/<int:pk>/', AnalysisDeleteView.as_view(), name='analysis_delete'),
]
