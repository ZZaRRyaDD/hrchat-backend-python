# Generated by Django 3.2.2 on 2022-09-21 16:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0001_initial'),
        ('trainings', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='trainer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rooms', to='users.trainer', verbose_name='Создатель комнаты'),
        ),
        migrations.AddField(
            model_name='message',
            name='in_round',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='trainings.round', verbose_name='Раунд'),
        ),
        migrations.AddField(
            model_name='message',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to=settings.AUTH_USER_MODEL, verbose_name='Автор сообщения'),
        ),
    ]
