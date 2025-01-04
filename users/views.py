from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.auth.views import LoginView
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, ListView

from services.models import Analysis, Appointment
from users.forms import UserLoginForm, UserRegisterForm, UserProfileUpdateForm, RequestModelForm
from users.models import User, Cart, History, Request
from users.services import send_email_verification


# Контроллеры относящиеся к модели User #############################
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


# Контроллеры относящиеся к модели Cart #############################
def get_cart_info(object_list):
    cart_count = 0
    cart_sum = 0

    if object_list is not None:
        cart_count = len(object_list)
        cart_sum = sum(obj.analysis.price + cart_sum or obj.appointmenp.price + cart_sum for obj in object_list)

    return cart_count, cart_sum


class CartListView(LoginRequiredMixin, ListView):
    """Контроллер для отображения списка объектов модели Cart."""
    model = Cart

    def get_context_data(self, *, object_list=None, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Корзина'

        user = self.request.user
        if user.groups.filter(name='user').exists():
            object_list = Cart.objects.filter(owner=user)
            context_data['object_list'] = object_list

            cart_count, cart_sum = get_cart_info(object_list)
            context_data['cart_count'] = cart_count
            context_data['cart_sum'] = cart_sum
            return context_data

        cart_count, cart_sum = get_cart_info(object_list)
        context_data['cart_count'] = cart_count
        context_data['cart_sum'] = cart_sum
        return context_data


@login_required
def add_to_cart(request):
    """Добавляет анализ или прием в корзину."""

    user = request.user
    obj_class = request.GET['type']
    pk = request.GET['id']

    if obj_class == 'analysis':
        Cart.objects.create(
            owner=user,
            analysis=Analysis.objects.get(pk=pk)
        )

    if obj_class == 'appointment':
        Cart.objects.create(
            owner=user,
            appointment=Appointment.objects.get(pk=pk)
        )

    return HttpResponse(status=201)


def delete_from_cart(request):
    """Удаляет объекты из корзины."""

    user = request.user
    pk = request.GET['id']

    Cart.objects.get(owner=user, pk=pk).delete()

    return HttpResponse(status=204)


# Контроллеры относящиеся к модели History ##########################
class HistoryListView(LoginRequiredMixin, ListView):
    """Контроллер для отображения списка объектов модели History."""
    model = History

    def get_context_data(self, *, object_list=None, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'История'

        user = self.request.user
        if user.groups.filter(name='user').exists():
            object_list = History.objects.filter(owner=user)
            context_data['object_list'] = object_list
            return context_data
        return context_data


class HistoryDetailView(LoginRequiredMixin, DetailView):
    """Контроллер для отображения объекта модели History."""
    model = History

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        user = self.request.user

        if user.groups.filter(name='user').exists():
            if user == self.object.owner:
                self.object.save()
                return self.object
            raise PermissionDenied

        self.object.save()
        return self.object

    def get_context_data(self, *, object_list=None, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'История'
        return context_data


# Контроллеры относящиеся к модели Request ##########################
class RequestCreateView(LoginRequiredMixin, CreateView):
    """Контроллер для создания объекта модели Request."""
    model = Request
    form_class = RequestModelForm
    success_url = reverse_lazy('users:profile')

    def form_valid(self, form):
        user = self.request.user
        request_obj = form.save()

        request_obj.owner = user
        request_obj.fullname = user.fullname
        request_obj.phone_number = user.phone_number
        request_obj.email = user.email

        request_obj.save()
        return super().form_valid(form)

    def get_context_data(self, *, object_list=None, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Запись на прием'
        return context_data
