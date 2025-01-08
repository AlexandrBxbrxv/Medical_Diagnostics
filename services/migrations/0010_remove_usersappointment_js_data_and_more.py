# Generated by Django 4.2.2 on 2025-01-08 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0009_usersappointment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usersappointment',
            name='js_data',
        ),
        migrations.AddField(
            model_name='usersappointment',
            name='service_id',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='id услуги'),
        ),
    ]
