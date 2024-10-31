from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser

from main.models import NULLABLE

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
    avatar = models.ImageField(upload_to='users/avatars', **NULLABLE, verbose_name='аватар')

    def __str__(self):
        return self.email

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
