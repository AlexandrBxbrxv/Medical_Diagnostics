from django.db import models


class Analysis(models.Model):
    """Модель анализа"""
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
