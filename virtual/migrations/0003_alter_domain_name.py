# Generated by Django 3.2.2 on 2021-05-08 21:00

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('virtual', '0002_auto_20210106_0100'),
    ]

    operations = [
        migrations.AlterField(
            model_name='domain',
            name='name',
            field=models.CharField(max_length=50, unique=True, validators=[django.core.validators.RegexValidator(message='Enter a valid domain name', regex='\\b((?=[a-z0-9-]{1,63}\\.)(xn--)?[a-z0-9]+(-[a-z0-9]+)*\\.)+[a-z]{2,63}\\b')]),
        ),
    ]
