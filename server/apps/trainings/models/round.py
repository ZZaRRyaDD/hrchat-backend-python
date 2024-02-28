from django.db import models
from django.utils.translation import ugettext_lazy as _

from .room import Room


class Round(models.Model):
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name='rounds',
        verbose_name=_('Комната раунда'),
    )

    class Meta:
        verbose_name = _('Раунд')
        verbose_name_plural = _('Раунды')

    def __str__(self) -> str:
        return f'Round of the room: {self.room}'
