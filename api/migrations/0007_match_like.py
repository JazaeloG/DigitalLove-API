# Generated by Django 4.2.11 on 2024-05-04 18:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_remove_usuario_user_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('usuario1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='matches1', to='api.usuario')),
                ('usuario2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='matches2', to='api.usuario')),
            ],
            options={
                'unique_together': {('usuario1', 'usuario2')},
            },
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accepted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes_received', to='api.usuario')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes_sent', to='api.usuario')),
            ],
            options={
                'unique_together': {('sender', 'receiver')},
            },
        ),
    ]