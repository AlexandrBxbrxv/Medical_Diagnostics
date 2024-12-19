from django.db import models

from config.settings import AUTH_USER_MODEL

NULLABLE = {'blank': True, 'null': True}

User = AUTH_USER_MODEL


class Feedback(models.Model):
    """Модель для обратной связи."""
    owner = models.ForeignKey(User, on_delete=models.CASCADE, **NULLABLE, related_name='feedbacks_owner',
                              verbose_name='владелец')
    fullname = models.CharField(max_length=150, verbose_name='Ф.И.О.')
    email = models.EmailField(verbose_name='email')
    message = models.TextField(verbose_name='сообщение')
    date_created = models.DateField(auto_now=True, verbose_name='время создания')
    is_closed = models.BooleanField(default=False, verbose_name='признак закрытости')
