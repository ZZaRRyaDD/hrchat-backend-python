from django.db import models
from django.utils.translation import ugettext_lazy as _

from .round import Round


class Message(models.Model):
    content = models.TextField(
        verbose_name=_('Тело сообщения'),
    )
    is_right = models.BooleanField(
        default=None,
        null=True,
        blank=True,
        verbose_name=_('Верное ли сообщение'),
    )
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name=_('Автор сообщения'),
    )
    in_round = models.ForeignKey(
        Round,
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name=_('Раунд'),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        blank=True,
        verbose_name=_('Время написания сообщения'),
    )

    class Meta:
        verbose_name = _('Сообщение')
        verbose_name_plural = _('Сообщения')

    def __str__(self) -> str:
        return (
            f'Message with content {self.content}, '
            f'written by {self.user} at {self.created_at}, '
            f'is_right: {self.is_right}'
        )
