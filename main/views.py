from django.views.generic import TemplateView


class IndexTemplateView(TemplateView):
    """Контроллер для отображения главной страницы."""
    template_name = 'main/index.html'
