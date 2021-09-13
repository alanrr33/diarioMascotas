# Generated by Django 3.2.3 on 2021-09-10 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alimentos', '0009_remove_alimentoconsumido_porcion'),
    ]

    operations = [
        migrations.AddField(
            model_name='alimento',
            name='tipo_mascota',
            field=models.CharField(choices=[('Gato', 'Gato'), ('Perro', 'Perro')], default='Gato', max_length=5),
        ),
    ]
