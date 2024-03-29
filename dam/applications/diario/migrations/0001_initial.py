# Generated by Django 3.2.3 on 2021-05-30 00:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('mascotas', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Diario',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('fecha', models.DateField(auto_now_add=True)),
                ('comidas', models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3')], default=2, max_length=1)),
                ('total_cal', models.PositiveIntegerField()),
                ('mascota', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mascotas.mascota')),
            ],
        ),
    ]
