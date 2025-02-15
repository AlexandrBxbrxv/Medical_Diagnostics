# Generated by Django 4.2.2 on 2024-10-31 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullname', models.CharField(max_length=150, verbose_name='Ф.И.О.')),
                ('speciality', models.CharField(max_length=200, verbose_name='специальность')),
                ('education', models.TextField(verbose_name='образование')),
                ('information', models.TextField(blank=True, null=True, verbose_name='общая информация')),
                ('experience', models.PositiveSmallIntegerField(verbose_name='стаж')),
            ],
            options={
                'verbose_name': 'врач',
                'verbose_name_plural': 'врачи',
            },
        ),
    ]
