# Generated by Django 3.2.3 on 2021-06-26 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diario', '0007_diario_dif_cal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diario',
            name='fecha',
            field=models.DateField(),
        ),
    ]
