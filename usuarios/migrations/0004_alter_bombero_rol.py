# Generated by Django 3.2 on 2024-07-12 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0003_actividad_hecha'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bombero',
            name='rol',
            field=models.CharField(choices=[('1', 'Jefe de Cuerpo'), ('2', 'Administrador'), ('3', 'Bombero')], max_length=1),
        ),
    ]
