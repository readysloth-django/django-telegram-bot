from django.db import models
from django.utils.translation import gettext_lazy as _

from solo.models import SingletonModel

from django_telegram_bot.aux import random_string


class Bot(SingletonModel):
    token = models.CharField(_('Token'), max_length=50)

    class Meta:
        verbose_name = _('Bot')
        verbose_name_plural = _('Bots')

    def __str__(self):
        return self.token


class AdminAccess(SingletonModel):
    key = models.CharField(_('Key'), max_length=8, default=random_string)

    class Meta:
        verbose_name = _('Admin access')
        verbose_name_plural = _('Admin accesses')

    def __str__(self):
        return self.key
