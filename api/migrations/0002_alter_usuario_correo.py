# Generated by Django 4.2.11 on 2024-05-29 20:03

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='correo',
            field=models.EmailField(max_length=50, unique=True, validators=[django.core.validators.EmailValidator()]),
        ),
    ]
