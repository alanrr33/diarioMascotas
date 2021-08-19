# Generated by Django 3.2.3 on 2021-05-30 01:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('diario', '0002_alter_diario_id'),
        ('alimentos', '0002_rename_fecha_comida_diario_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comida',
            name='diario_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comidadiario', to='diario.diario'),
        ),
    ]
