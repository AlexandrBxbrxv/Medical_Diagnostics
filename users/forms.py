from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm

from main.forms import StyleFormMixin
from users.models import User


class UserLoginForm(StyleFormMixin, AuthenticationForm):
    pass


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'fullname', 'phone_number', 'password1', 'password2',)


class UserProfileUpdateForm(StyleFormMixin, UserChangeForm):
    class Meta:
        model = User
        fields = ('fullname', 'phone_number',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.HiddenInput()
