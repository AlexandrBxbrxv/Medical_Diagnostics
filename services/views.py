from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from services.forms import DoctorModelForm
from services.models import Doctor


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


class DoctorListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """Контроллер для отображения списка объектов модели Doctor."""
    model = Doctor
    permission_required = 'services.view_doctor'

    def get_context_data(self, *, object_list=None, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Команда врачей'

        user = self.request.user
        if user.is_superuser:
            return context_data

        users_items = []
        for item in context_data.get('object_list'):
            if user == item.owner:
                users_items.append(item)
        context_data['object_list'] = users_items
        return context_data


class DoctorDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    """Контроллер для отображения объекта модели Doctor."""
    model = Doctor
    permission_required = 'services.view_doctor'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        user = self.request.user
        if user == self.object.owner or user.is_superuser:
            self.object.save()
            return self.object
        raise PermissionDenied

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
        if user == self.object.owner or user.is_superuser:
            self.object.save()
            return self.object
        raise PermissionDenied

    def get_success_url(self):
        return reverse('service:doctor_detail', args=[self.kwargs.get('pk')])

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
        if user == self.object.owner or user.is_superuser:
            self.object.save()
            return self.object
        raise PermissionDenied

    def get_context_data(self, *, object_list=None, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Удаление врача'
        return context_data
