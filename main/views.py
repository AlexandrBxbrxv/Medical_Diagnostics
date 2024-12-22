from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import TemplateView

from main.models import Feedback
from services.models import Doctor
from users.models import User


class IndexTemplateView(TemplateView):
    """Контроллер для отображения главной страницы."""
    template_name = 'main/index.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Главная'
        return context_data


class AboutTemplateView(TemplateView):
    """Контроллер для отображения страницы о компании."""
    template_name = 'main/about.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'О компании'
        context_data['doctor_count'] = Doctor.objects.count()
        return context_data


class ContactsTemplateView(TemplateView):
    """Контроллер для отображения страницы контакты."""
    template_name = 'main/contacts.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Контакты'
        return context_data


def feedback(request):
    """Для отправки обратной связи."""

    user = None

    if isinstance(request.user, User):
        user = request.user

    fullname = request.POST.get("fullname")
    email = request.POST.get("email")
    message = request.POST.get("message")

    if fullname and email and message:

        Feedback.objects.create(
            owner=user,
            fullname=fullname,
            email=email,
            message=message
        )

    return HttpResponseRedirect(reverse('main:index'))
