# Generated by Django 4.2.11 on 2024-05-18 19:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_usuario_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='like',
            name='envia',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='like_envia', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='like',
            name='recibe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='like_recibe', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='reporte',
            name='motivo',
            field=models.CharField(choices=[('ACOSO', 'Acoso'), ('SPAM', 'Spam'), ('CONTENIDO_INAPROPIADO', 'Contenido inapropiado'), ('FRAUDE', 'Fraude')], default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='reporte',
            name='usuario_reportado',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reportes_recibidos', to=settings.AUTH_USER_MODEL),
        ),
    ]
