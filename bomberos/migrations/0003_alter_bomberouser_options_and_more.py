# Generated by Django 4.1.2 on 2023-04-25 20:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bomberos', '0002_categoriabombero_codigoarea_bomberouser_apellido_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bomberouser',
            options={'verbose_name_plural': 'Bomberos'},
        ),
        migrations.AlterField(
            model_name='bomberouser',
            name='categoria',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='bomberos', to='bomberos.categoriabombero'),
        ),
        migrations.AlterField(
            model_name='categoriabombero',
            name='descripcion',
            field=models.TextField(blank=True, null=True),
        ),
    ]
