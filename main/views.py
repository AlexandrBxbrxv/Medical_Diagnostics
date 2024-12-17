from django.views.generic import TemplateView

from services.models import Doctor


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
