# Generated by Django 3.2.3 on 2021-08-20 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20210819_1352'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='cod_registro',
            field=models.CharField(blank=True, max_length=6),
        ),
    ]
