from django.db import models
from django.utils.translation import ugettext_lazy as _


class Student(models.Model):
    full_name = models.CharField(
        max_length=128,
        verbose_name=_('ФИО пользователя'),
    )
    user = models.OneToOneField(
        'users.User',
        on_delete=models.CASCADE,
        related_name='student',
        verbose_name=_('Пользователь'),
    )
    is_ready = models.BooleanField(
        default=False,
        verbose_name=_('Готов ли пользователь к испытанию'),
    )
    room = models.ForeignKey(
        'trainings.Room',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='students',
        verbose_name=_('Комната'),
    )
    is_kicked = models.BooleanField(
        default=False,
        verbose_name=_('Исключен ли студент'),
    )

    class Meta:
        verbose_name = _('Студент')
        verbose_name_plural = _('Студенты')

    def __str__(self) -> str:
        return f'Student of user {self.user}'
