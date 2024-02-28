# Generated by Django 3.2.2 on 2022-09-21 16:54

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='Тело сообщения')),
                ('is_right', models.BooleanField(blank=True, default=None, null=True, verbose_name='Верное ли сообщение')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Время написания сообщения')),
            ],
            options={
                'verbose_name': 'Сообщение',
                'verbose_name_plural': 'Сообщения',
            },
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('max_students', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(2), django.core.validators.MaxValueValidator(15)], verbose_name='Максимальное количество студентов в комнате')),
                ('max_rounds', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(2)], verbose_name='Максимальное количество раундов')),
                ('max_duration_round', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(15), django.core.validators.MaxValueValidator(60)], verbose_name='Максимальная длительность раунда')),
                ('is_started', models.BooleanField(default=False, verbose_name='Начат ли матч')),
                ('is_finished', models.BooleanField(default=False, verbose_name='Завершен ли матч')),
            ],
            options={
                'verbose_name': 'Комната',
                'verbose_name_plural': 'Комнаты',
            },
        ),
        migrations.CreateModel(
            name='Round',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rounds', to='trainings.room', verbose_name='Комната раунда')),
            ],
            options={
                'verbose_name': 'Раунд',
                'verbose_name_plural': 'Раунды',
            },
        ),
    ]
