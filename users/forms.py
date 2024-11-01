from django.contrib.auth.forms import AuthenticationForm

from main.forms import StyleFormMixin


class UserLoginForm(StyleFormMixin, AuthenticationForm):
    pass
