# Generated by Django 3.2.3 on 2021-05-31 22:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diario', '0003_auto_20210530_1224'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diario',
            name='total_cal',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
