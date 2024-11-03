from django.contrib.auth.forms import AuthenticationForm
from django.forms import ModelForm

from main.forms import StyleFormMixin
from users.models import User


class UserLoginForm(StyleFormMixin, AuthenticationForm):
    pass


class UserRegisterForm(StyleFormMixin, ModelForm):
    class Meta:
        model = User
        fields = ('email', 'fullname', 'phone_number', 'password1', 'password2',)
