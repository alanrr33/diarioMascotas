# Generated by Django 3.2.3 on 2021-08-26 17:16

import django.contrib.auth.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_user_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=20, unique=True, validators=[django.contrib.auth.validators.ASCIIUsernameValidator(message='Ingrese un nombre de usuario valido.Letras, numeros, y los caracteres @/./+/-/_ ')]),
        ),
    ]