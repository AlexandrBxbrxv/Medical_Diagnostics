from django.forms import ModelForm

from main.forms import StyleFormMixin
from services.models import Doctor


class DoctorModelForm(StyleFormMixin, ModelForm):
    """Форма для создания/редактирования модели Doctor"""
    class Meta:
        model = Doctor
        exclude = ('owner',)
