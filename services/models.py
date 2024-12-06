from django.db import models

from main.models import NULLABLE
from config.settings import AUTH_USER_MODEL

User = AUTH_USER_MODEL


class Doctor(models.Model):
    """Модель врача, врач не является пользователем сайта."""
    owner = models.ForeignKey(User, on_delete=models.CASCADE, **NULLABLE, related_name='doctors_owner',
                              verbose_name='владелец')
    fullname = models.CharField(max_length=150, verbose_name='Ф.И.О.')
    speciality = models.CharField(max_length=200, verbose_name='специальность')
    education = models.TextField(verbose_name='образование')
    information = models.TextField(**NULLABLE, verbose_name='общая информация')
    avatar = models.ImageField(upload_to='services/avatars', default='avatar_placeholder.jpg', **NULLABLE,
                               verbose_name='аватар')

    experience = models.PositiveSmallIntegerField(verbose_name='стаж')

    def __str__(self):
        return self.fullname

    class Meta:
        verbose_name = 'врач'
        verbose_name_plural = 'врачи'


class Appointment(models.Model):
    """Модель записи на прием ко врачу."""
    owner = models.ForeignKey(User, on_delete=models.CASCADE, **NULLABLE, related_name='appointments_owner',
                              verbose_name='владелец')
    title = models.CharField(max_length=200, verbose_name='название')

    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, **NULLABLE, related_name='appointments_doctor',
                               verbose_name='врач')

    date_time = models.DateTimeField(**NULLABLE, verbose_name='дата и время приема')
    treatment_room = models.PositiveSmallIntegerField(verbose_name='процедурный кабинет')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'прием'
        verbose_name_plural = 'приемы'


class Service(models.Model):
    """Модель услуги на приеме."""
    owner = models.ForeignKey(User, on_delete=models.CASCADE, **NULLABLE, related_name='services_owner',
                              verbose_name='владелец')
    title = models.CharField(max_length=200, verbose_name='название')
    description = models.TextField(verbose_name='описание')
    preparation = models.TextField(default='Особой подготовки не требуется.', verbose_name='подготовка')
    price = models.PositiveSmallIntegerField(verbose_name='цена')

    appointment = models.ForeignKey(Appointment, on_delete=models.SET_NULL, **NULLABLE,
                                    related_name='services_appointment', verbose_name='запись')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'услуга'
        verbose_name_plural = 'услуги'
        ordering = ('price',)


class Analysis(models.Model):
    """Модель анализа."""
    owner = models.ForeignKey(User, on_delete=models.CASCADE, **NULLABLE, related_name='analyses_owner',
                              verbose_name='владелец')
    title = models.CharField(max_length=200, verbose_name='название')
    description = models.TextField(verbose_name='описание')
    preparation = models.TextField(default='Особой подготовки не требуется.', verbose_name='подготовка')

    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, **NULLABLE, related_name='analyses_doctor',
                               verbose_name='врач')

    date_time = models.DateTimeField(**NULLABLE, verbose_name='дата и время приема')
    treatment_room = models.PositiveSmallIntegerField(verbose_name='процедурный кабинет')
    price = models.PositiveSmallIntegerField(verbose_name='цена')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'анализ'
        verbose_name_plural = 'анализы'
        ordering = ('price',)


class Result(models.Model):
    """Модель результата анализа или диагноза на приеме."""
    owner = models.ForeignKey(User, on_delete=models.CASCADE, **NULLABLE, related_name='results_owner',
                              verbose_name='владелец')
    title = models.CharField(max_length=200, verbose_name='название')

    analysis = models.ForeignKey(Analysis, on_delete=models.SET_NULL, **NULLABLE, related_name='results_analysis',
                                 verbose_name='анализ')
    appointment = models.ForeignKey(Appointment, on_delete=models.SET_NULL, **NULLABLE,
                                    related_name='results_appointment', verbose_name='прием')

    message = models.TextField(help_text='Результат анализа или диагноз приема', verbose_name='сообщение')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'результат'
        verbose_name_plural = 'результаты'
