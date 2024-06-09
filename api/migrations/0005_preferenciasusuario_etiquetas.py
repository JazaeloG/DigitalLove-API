# Generated by Django 4.2.11 on 2024-06-03 20:15

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_remove_usuario_latitud_remove_usuario_longitud'),
    ]

    operations = [
        migrations.AddField(
            model_name='preferenciasusuario',
            name='etiquetas',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=50), choices=[('AMOR', 'Amor'), ('VIDEOJUEGOS', 'Videojuegos'), ('DEPORTES', 'Deportes'), ('MUSICA', 'Musica'), ('PELICULAS', 'Películas'), ('SERIES', 'Series'), ('ANIME', 'Anime'), ('VIAJAR', 'Viajar'), ('GYM', 'Gym'), ('LECTURA', 'Lectura'), ('COCINAR', 'Cocinar'), ('FOTOGRAFIA', 'Fotografia'), ('SENDERISMO', 'Senderismo'), ('NATURALEZA', 'Naturaleza'), ('MODA', 'Moda'), ('BAILAR', 'Bailar')], default=list, size=None),
        ),
    ]