from django.urls import path

from main.apps import MainConfig
from main.views import IndexTemplateView, AboutTemplateView, ContactsTemplateView, feedback

app_name = MainConfig.name

urlpatterns = [
    path('', IndexTemplateView.as_view(), name='index'),
    path('about/', AboutTemplateView.as_view(), name='about'),
    path('contacts/', ContactsTemplateView.as_view(), name='contacts'),
    path('feedback/', feedback, name='feedback')
]
