from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.forms import inlineformset_factory
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from services.forms import DoctorModelForm, AppointmentModelForm, AnalysisModelForm, ResultModelForm
from services.models import Doctor, Appointment, Service, Analysis, Result


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
        appointment = form.save()
        user = self.request.user
        appointment.owner = user
        appointment.save()
        return super().form_valid(form)

    def get_context_data(self, *, object_list=None, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Добавление записи на прием'
        return context_data


class AppointmentListView(ListView):
    """Контроллер для отображения списка объектов модели Appointment."""
    model = Appointment

    def get_context_data(self, *, object_list=None, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Список приемов'

        user = self.request.user
        if user.groups.filter(name='medical_staff').exists():
            users_items = []
            for item in context_data.get('object_list'):
                if user == item.owner:
                    users_items.append(item)
            context_data['object_list'] = users_items
            return context_data
        return context_data


class AppointmentDetailView(DetailView):
    """Контроллер для отображения объекта модели Appointment."""
    model = Appointment

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
        context_data['title'] = 'Прием'
        return context_data


class AppointmentUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Контроллер для изменения объекта модели Appointment и добавления к нему объектов модели Service."""
    model = Appointment
    form_class = AppointmentModelForm
    permission_required = 'services.change_appointment'

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

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('services:appointment_detail', args=[self.kwargs.get('pk')])

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        AppointmentFormset = inlineformset_factory(Appointment, Service, form=AppointmentModelForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = AppointmentFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = AppointmentFormset(instance=self.object)
        return context_data


class AppointmentDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """Контроллер для удаления объекта модели Appointment."""
    model = Appointment
    permission_required = 'services.delete_appointment'
    success_url = reverse_lazy('services:appointment_list')

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
        context_data['title'] = 'Удаление приема'
        return context_data


# CRUD для модели Analysis ##########################################
class AnalysisCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Контроллер для создания объекта модели Analysis."""
    model = Analysis
    form_class = AnalysisModelForm
    permission_required = 'services.add_analysis'
    success_url = reverse_lazy('services:analysis_create')

    def form_valid(self, form):
        analysis = form.save()
        user = self.request.user
        analysis.owner = user
        analysis.save()
        return super().form_valid(form)

    def get_context_data(self, *, object_list=None, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Добавление анализа'
        return context_data


class AnalysisListView(ListView):
    """Контроллер для отображения списка объектов модели Analysis."""
    model = Analysis

    def get_context_data(self, *, object_list=None, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Список анализов'

        user = self.request.user
        if user.groups.filter(name='medical_staff').exists():
            users_items = []
            for item in context_data.get('object_list'):
                if user == item.owner:
                    users_items.append(item)
            context_data['object_list'] = users_items
            return context_data
        return context_data


class AnalysisDetailView(DetailView):
    """Контроллер для отображения объекта модели Analysis."""
    model = Analysis

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
        context_data['title'] = 'Анализ'
        return context_data


class AnalysisUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Контроллер для редактирования объекта модели Analysis."""
    model = Analysis
    form_class = AnalysisModelForm
    permission_required = 'services.change_analysis'

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
        return reverse('services:analysis_detail', args=[self.kwargs.get('pk')])

    def get_context_data(self, *, object_list=None, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Редактирование анализа'
        return context_data


class AnalysisDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """Контроллер для удаления объекта модели Analysis."""
    model = Analysis
    permission_required = 'services.delete_analysis'
    success_url = reverse_lazy('services:analysis_list')

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
        context_data['title'] = 'Удаление анализа'
        return context_data


# CRUD для модели Result ############################################
class ResultCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Контроллер для создания объекта модели Result."""
    model = Result
    form_class = ResultModelForm
    permission_required = 'services.add_result'
    success_url = reverse_lazy('services:result_create')

    def form_valid(self, form):
        result = form.save()
        user = self.request.user
        result.owner = user
        result.save()
        return super().form_valid(form)

    def get_context_data(self, *, object_list=None, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Добавление результата'
        return context_data


class ResultListView(ListView):
    """Контроллер для отображения списка объектов модели Result."""
    model = Result

    def get_context_data(self, *, object_list=None, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Список результатов'

        user = self.request.user
        if user.groups.filter(name='medical_staff').exists():
            users_items = []
            for item in context_data.get('object_list'):
                if user == item.owner:
                    users_items.append(item)
            context_data['object_list'] = users_items
            return context_data
        return context_data


class ResultDetailView(DetailView):
    """Контроллер для отображения объекта модели Result."""
    model = Result

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
        context_data['title'] = 'Результат'
        return context_data


class ResultUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Контроллер для редактирования объекта модели Result."""
    model = Result
    form_class = ResultModelForm
    permission_required = 'services.change_result'

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
        return reverse('services:result_detail', args=[self.kwargs.get('pk')])

    def get_context_data(self, *, object_list=None, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Редактирование результата'
        return context_data


class ResultDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """Контроллер для удаления объекта модели Result."""
    model = Result
    permission_required = 'services.delete_result'
    success_url = reverse_lazy('services:result_list')

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
        context_data['title'] = 'Удаление результата'
        return context_data
