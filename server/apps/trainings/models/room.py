import uuid

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _

from ..constants import RoomConstants


class Room(models.Model):
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    trainer = models.ForeignKey(
        'users.Trainer',
        on_delete=models.CASCADE,
        related_name='rooms',
        verbose_name=_('Создатель комнаты'),
    )
    max_students = models.PositiveIntegerField(
        validators=[
            MinValueValidator(RoomConstants.MIN_COUNT_STUDENT),
            MaxValueValidator(RoomConstants.MAX_COUNT_STUDENT),
        ],
        verbose_name=_('Максимальное количество студентов в комнате'),
    )
    max_rounds = models.PositiveIntegerField(
        validators=[
            MinValueValidator(RoomConstants.MIN_COUNT_ROUNDS),
        ],
        verbose_name=_('Максимальное количество раундов'),
    )
    max_duration_round = models.PositiveIntegerField(
        validators=[
            MinValueValidator(RoomConstants.MIN_DURATION),
            MaxValueValidator(RoomConstants.MAX_DURATION),
        ],
        verbose_name=_('Максимальная длительность раунда'),
    )
    is_started = models.BooleanField(
        default=False,
        verbose_name=_('Начат ли матч'),
    )
    is_finished = models.BooleanField(
        default=False,
        verbose_name=_('Завершен ли матч'),
    )

    class Meta:
        verbose_name = _('Комната')
        verbose_name_plural = _('Комнаты')

    def __str__(self) -> str:
        return (
            f'Room with {self.max_students} students, '
            f'{self.max_rounds} rounds, '
            f'{self.max_duration_round} duration of round '
            f'and trainer {self.trainer}'
        )
