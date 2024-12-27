from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser

from main.models import NULLABLE
from services.models import Analysis, Appointment, Result

phone_validation = RegexValidator(
    regex=r'^(?:\+7|8)\d{10}$',  # Проверка для российских номеров телефона
    message="Номер телефона должен быть в формате '+7XXXXXXXXXX' или '8XXXXXXXXXX'."
)


class User(AbstractUser):
    """Кастомный пользователь."""
    username = None

    email = models.EmailField(unique=True, verbose_name='email')
    token = models.CharField(max_length=50, **NULLABLE, verbose_name='token')

    fullname = models.CharField(max_length=150, verbose_name='Ф.И.О.')
    phone_number = models.CharField(unique=True, max_length=12, validators=[phone_validation],
                                    verbose_name='номер телефона')
    avatar = models.ImageField(upload_to='users/avatars', default='avatar_placeholder.jpg', **NULLABLE,
                               verbose_name='аватар')

    def __str__(self):
        return self.email

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'


class Cart(models.Model):
    """Модель корзины для набора анализов и приемов для последующей оплаты."""
    owner = models.ForeignKey(User, on_delete=models.CASCADE, **NULLABLE, related_name='carts_owner',
                              verbose_name='владелец')
    analysis = models.ForeignKey(Analysis, on_delete=models.CASCADE, **NULLABLE, related_name='carts_analysis',
                                 verbose_name='анализ')
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, **NULLABLE,
                                    related_name='carts_appointment', verbose_name='прием')

    class Meta:
        verbose_name = 'козина'
        verbose_name_plural = 'корзины'


class History(models.Model):
    """Модель истории для записи всех оплаченных услуг и результатов."""
    owner = models.ForeignKey(User, on_delete=models.CASCADE, **NULLABLE, related_name='histories_owner',
                              verbose_name='владелец')
    payment_daytime = models.DateTimeField(auto_now=True, verbose_name='дата и время оплаты')
    service_info = models.TextField(**NULLABLE, verbose_name='информация об услуге')
    price = models.PositiveIntegerField(default=0, verbose_name='цена')

    result = models.ForeignKey(Result, on_delete=models.SET_NULL, **NULLABLE, related_name='histories_result',
                               verbose_name='результат')

    class Meta:
        verbose_name = 'история'
        verbose_name_plural = 'истории'
        ordering = ('-payment_daytime',)
