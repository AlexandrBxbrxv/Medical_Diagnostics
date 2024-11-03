# Generated by Django 4.2.2 on 2024-10-31 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Analysis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='название')),
                ('description', models.TextField(verbose_name='описание')),
                ('preparation', models.TextField(verbose_name='подготовка')),
                ('treatment_room', models.PositiveSmallIntegerField(verbose_name='процедурный кабинет')),
                ('price', models.PositiveSmallIntegerField(verbose_name='цена')),
            ],
            options={
                'verbose_name': 'анализ',
                'verbose_name_plural': 'анализы',
                'ordering': ('price',),
            },
        ),
    ]