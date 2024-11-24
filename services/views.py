from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView

from services.forms import DoctorModelForm
from services.models import Doctor


# CRUD для модели Doctor ############################################
class DoctorCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Контроллер для создания объекта модели Doctor"""
    model = Doctor
    form_class = DoctorModelForm
    permission_required = 'services.add_doctor'
    success_url = reverse_lazy('services:doctor_create')

    def form_valid(self, form):
        doctor = form.save()
        user = self.request.user
        doctor.owner = user
        doctor.save()
        return super().form_valid(form)

    def get_context_data(self, *, object_list=None, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Добавление врача'
        return context_data
