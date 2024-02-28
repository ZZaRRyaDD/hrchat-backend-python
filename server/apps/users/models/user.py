from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

from .trainer import Trainer


class User(AbstractUser):

    @property
    def is_trainer(self) -> bool:
        try:
            return self.trainer is not None
        except Trainer.DoesNotExist:
            return False

    class Meta:
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')

    def __str__(self) -> str:
        return (
            f'{self.username}, '
            f'is_trainer {self.is_trainer}'
        )
