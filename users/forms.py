from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.forms import ModelForm, DateInput

from main.forms import StyleFormMixin
from users.models import User, Request


class UserLoginForm(StyleFormMixin, AuthenticationForm):
    pass


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    """Форма для создания объекта модели User."""

    class Meta:
        model = User
        fields = ('email', 'fullname', 'phone_number', 'password1', 'password2',)


class UserProfileUpdateForm(StyleFormMixin, UserChangeForm):
    """Форма для редактирования объекта модели User."""

    class Meta:
        model = User
        fields = ('fullname', 'phone_number',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.HiddenInput()


class RequestModelForm(StyleFormMixin, ModelForm):
    """Форма для создания/редактирования объекта модели Request."""

    class Meta:
        model = Request
        exclude = ('owner', 'fullname', 'phone_number', 'email',)
