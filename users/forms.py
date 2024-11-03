from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from main.forms import StyleFormMixin
from users.models import User


class UserLoginForm(StyleFormMixin, AuthenticationForm):
    pass


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'fullname', 'phone_number', 'password1', 'password2',)
