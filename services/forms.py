from django.forms import ModelForm

from main.forms import StyleFormMixin
from services.models import Doctor, Appointment


class DoctorModelForm(StyleFormMixin, ModelForm):
    """Форма для создания/редактирования модели Doctor"""
    class Meta:
        model = Doctor
        exclude = ('owner',)


class AppointmentModelForm(StyleFormMixin, ModelForm):
    """Форма для создания/редактирования модели Doctor"""
    class Meta:
        model = Appointment
        exclude = ('owner',)
