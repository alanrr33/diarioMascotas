# Generated by Django 3.2.3 on 2021-06-08 01:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mascotas', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mascota',
            options={'ordering': ['id']},
        ),
    ]
