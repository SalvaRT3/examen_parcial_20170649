# Generated by Django 4.2 on 2023-04-15 03:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_tienda', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datosusuario',
            name='nroCelular',
            field=models.CharField(default='000000000', max_length=32),
        ),
    ]