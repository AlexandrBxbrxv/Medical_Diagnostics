from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.auth.views import LoginView
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView

from users.forms import UserLoginForm, UserRegisterForm, UserProfileUpdateForm
from users.models import User
from users.services import send_email_verification


class UserLoginView(LoginView):
    """Контроллер для логина пользователя."""
    template_name = 'users/login.html'
    form_class = UserLoginForm

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Авторизация'
        return context_data


class UserRegister(CreateView):
    """Контроллер для регистрации пользователя."""
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('main:index')

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        user.save()
        send_email_verification(self, user)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Регистрация'
        return context_data


def email_verification(request, token):
    """Находит пользователя по токену из ссылки, выдает группу user и активирует пользователя."""
    user = get_object_or_404(User, token=token)

    user_group = Group.objects.get(name='user')
    user_group.user_set.add(user)

    user.is_active = True
    user.save()
    return redirect('users:login')


class UserProfile(LoginRequiredMixin, DetailView):
    """Контроллер просмотра профиля пользователя."""
    model = User
    template_name = 'users/profile.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Профиль'
        return context


class UserProfileUpdate(LoginRequiredMixin, UpdateView):
    """Контроллер редактирования профиля пользователя."""
    model = User
    form_class = UserProfileUpdateForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактирование профиля'
        return context
