# Generated by Django 3.2.3 on 2021-06-03 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diario', '0004_alter_diario_total_cal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diario',
            name='total_cal',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
    ]
