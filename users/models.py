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


class Request(models.Model):
    """Модель для оставления заявки на прием."""
    SPECIALIZATION_CHOICES = [
        ('choose', 'Выберите специалиста'),
        ('therapist', 'Терапевт'),
        ('surgeon', 'Хирург'),
        ('ultrasound', 'УЗИ'),
        ('gastroenterologist', 'Гастроэнтеролог'),
        ('dermatologist', 'Дерматолог'),
        ('cardiologist', 'Кардиолог'),
        ('otorhinolaryngologist', 'Оториноларинголог'),
        ('neurologist', 'Невролог'),
        ('urologist', 'Уролог'),
    ]

    TIME_CHOICES = [
        ('08_30', '08:30'),
        ('09_00', '09:00'),
        ('09_30', '09:30'),
        ('10_00', '10:00'),
        ('10_30', '10:30'),
        ('11_00', '11:00'),
        ('11_30', '11:30'),
        ('12_00', '12:00'),
        ('12_30', '12:30'),
        ('13_00', '13:00'),
        ('13_30', '13:30'),
        ('14_00', '14:00'),
        ('14_30', '14:30'),
        ('15_00', '15:00'),
        ('15_30', '15:30'),
        ('16_00', '16:00'),
        ('16_30', '16:30'),
        ('17_00', '17:00'),
        ('17_30', '17:30'),
        ('18_00', '18:00'),
        ('18_30', '18:30'),
        ('19_00', '19:00'),
        ('19_30', '19:30'),
    ]

    FROM_TIME_CHOICES = [
        ('08_00', '08:00'),
    ] + TIME_CHOICES

    TO_TIME_CHOICES = TIME_CHOICES + [
        ('20_00', '20:00')
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE, **NULLABLE, related_name='requests_owner',
                              verbose_name='владелец')
    specialization = models.CharField(max_length=30, choices=SPECIALIZATION_CHOICES, default='choose',
                                      verbose_name='специализация')
    date = models.DateField(verbose_name='дата')
    from_time = models.CharField(max_length=5, choices=FROM_TIME_CHOICES, default='08_00', verbose_name='с')
    to_time = models.CharField(max_length=5, choices=TO_TIME_CHOICES, default='20_00', verbose_name='до')

    fullname = models.CharField(max_length=150, **NULLABLE, verbose_name='Ф.И.О.')
    phone_number = models.CharField(max_length=12, **NULLABLE, verbose_name='номер телефона')
    email = models.EmailField(**NULLABLE, verbose_name='email')

    comment = models.TextField(verbose_name='комментарий')

    class Meta:
        verbose_name = 'заявка'
        verbose_name_plural = 'заявки на запись на прием'
        ordering = ('-date',)
