from django.db import models
from django.utils.translation import ugettext_lazy as _


class Trainer(models.Model):
    user = models.OneToOneField(
        'users.User',
        on_delete=models.CASCADE,
        related_name='trainer',
        verbose_name=_('Пользователь'),
    )

    class Meta:
        verbose_name = _('Тренер')
        verbose_name_plural = _('Тренера')

    def __str__(self) -> str:
        return f'Trainer of user {self.user}'
