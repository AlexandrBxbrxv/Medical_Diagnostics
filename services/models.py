from django.db import models

from main.models import NULLABLE


class Doctor(models.Model):
    """Модель врача, врач не является пользователем сайта."""
    fullname = models.CharField(max_length=150, verbose_name='Ф.И.О.')
    speciality = models.CharField(max_length=200, verbose_name='специальность')
    education = models.TextField(verbose_name='образование')
    information = models.TextField(**NULLABLE, verbose_name='общая информация')

    experience = models.PositiveSmallIntegerField(verbose_name='стаж')

    def __str__(self):
        return self.fullname

    class Meta:
        verbose_name = 'врач'
        verbose_name_plural = 'врачи'


class Appointment(models.Model):
    """Модель записи на приём ко врачу."""
    title = models.CharField(max_length=200, verbose_name='название')
    description = models.TextField(verbose_name='описание')

    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, **NULLABLE, related_name='appointments_doctor',
                               verbose_name='врач')

    treatment_room = models.PositiveSmallIntegerField(verbose_name='процедурный кабинет')
    price = models.PositiveSmallIntegerField(verbose_name='цена')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'прием'
        verbose_name_plural = 'приемы'
        ordering = ('price',)


class Analysis(models.Model):
    """Модель анализа."""
    title = models.CharField(max_length=200, verbose_name='название')
    description = models.TextField(verbose_name='описание')
    preparation = models.TextField(verbose_name='подготовка')

    treatment_room = models.PositiveSmallIntegerField(verbose_name='процедурный кабинет')
    price = models.PositiveSmallIntegerField(verbose_name='цена')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'анализ'
        verbose_name_plural = 'анализы'
        ordering = ('price',)
