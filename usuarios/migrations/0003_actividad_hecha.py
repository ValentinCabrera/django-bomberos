# Generated by Django 3.2 on 2024-05-31 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0002_auto_20240525_1553'),
    ]

    operations = [
        migrations.AddField(
            model_name='actividad',
            name='hecha',
            field=models.BooleanField(default=False),
        ),
    ]
