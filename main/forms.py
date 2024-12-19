from django.forms import BooleanField, ModelForm

from main.models import Feedback


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'


class FeedbackModelForm(StyleFormMixin, ModelForm):
    """Форма для создания/редактирования объекта модели Feedback."""

    class Meta:
        model = Feedback
        exclude = ('owner', 'date_created', 'is_closed')
