from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from services.forms import DoctorModelForm, AppointmentModelForm
from services.models import Doctor, Appointment


# CRUD для модели Doctor ############################################
class DoctorCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Контроллер для создания объекта модели Doctor."""
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


class DoctorListView(ListView):
    """Контроллер для отображения списка объектов модели Doctor."""
    model = Doctor

    def get_context_data(self, *, object_list=None, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Команда врачей'

        user = self.request.user
        if user.groups.filter(name='medical_staff').exists():
            users_items = []
            for item in context_data.get('object_list'):
                if user == item.owner:
                    users_items.append(item)
            context_data['object_list'] = users_items
            return context_data
        return context_data


class DoctorDetailView(DetailView):
    """Контроллер для отображения объекта модели Doctor."""
    model = Doctor

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        user = self.request.user

        if user.groups.filter(name='medical_staff').exists():
            if user == self.object.owner:
                self.object.save()
                return self.object
            raise PermissionDenied

        self.object.save()
        return self.object

    def get_context_data(self, *, object_list=None, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Информация о враче'
        return context_data


class DoctorUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Контроллер для редактирования объекта модели Doctor."""
    model = Doctor
    form_class = DoctorModelForm
    permission_required = 'services.change_doctor'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        user = self.request.user

        if user.groups.filter(name='medical_staff').exists():
            if user == self.object.owner:
                self.object.save()
                return self.object
            raise PermissionDenied

        self.object.save()
        return self.object

    def get_success_url(self):
        return reverse('services:doctor_detail', args=[self.kwargs.get('pk')])

    def get_context_data(self, *, object_list=None, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Редактирование врача'
        return context_data


class DoctorDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """Контроллер для удаления объекта модели Doctor."""
    model = Doctor
    permission_required = 'services.delete_doctor'
    success_url = reverse_lazy('services:doctor_list')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        user = self.request.user

        if user.groups.filter(name='medical_staff').exists():
            if user == self.object.owner:
                self.object.save()
                return self.object
            raise PermissionDenied

        self.object.save()
        return self.object

    def get_context_data(self, *, object_list=None, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Удаление врача'
        return context_data


# CRUD для Appointment ##############################################
class AppointmentCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Контроллер для создания объекта модели Appointment."""
    model = Appointment
    form_class = AppointmentModelForm
    permission_required = 'services.add_appointment'
    success_url = reverse_lazy('services:appointment_create')

    def form_valid(self, form):
        doctor = form.save()
        user = self.request.user
        doctor.owner = user
        doctor.save()
        return super().form_valid(form)

    def get_context_data(self, *, object_list=None, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Добавление записи на прием'
        return context_data
