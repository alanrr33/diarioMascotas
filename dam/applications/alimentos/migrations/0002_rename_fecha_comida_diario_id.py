# Generated by Django 3.2.3 on 2021-05-30 00:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alimentos', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comida',
            old_name='fecha',
            new_name='diario_id',
        ),
    ]
