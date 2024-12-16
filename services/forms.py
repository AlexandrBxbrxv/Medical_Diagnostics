from django.forms import ModelForm

from main.forms import StyleFormMixin
from services.models import Doctor, Appointment, Analysis, Result


class DoctorModelForm(StyleFormMixin, ModelForm):
    """Форма для создания/редактирования объекта модели Doctor."""
    class Meta:
        model = Doctor
        exclude = ('owner',)


class AppointmentModelForm(StyleFormMixin, ModelForm):
    """Форма для создания/редактирования объекта модели Doctor."""
    class Meta:
        model = Appointment
        exclude = ('owner',)


class AnalysisModelForm(StyleFormMixin, ModelForm):
    """Форма для создания/редактирования объекта модели Analysis."""

    class Meta:
        model = Analysis
        exclude = ('owner',)


class ResultModelForm(StyleFormMixin, ModelForm):
    """Форма для создания/редактирования объекта модели Result."""

    class Meta:
        model = Result
        exclude = ('owner',)
