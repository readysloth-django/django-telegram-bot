from django.db import models

from solo.models import SingletonModel

from django_telegram_bot.aux import random_string


class Bot(SingletonModel):
    token = models.CharField('Token', max_length=50)

    class Meta:
        verbose_name = 'Bot'
        verbose_name_plural = 'Bots'

    def __str__(self):
        return self.token


class AdminAccess(SingletonModel):
    key = models.CharField('Key', max_length=8, default=random_string)

    class Meta:
        verbose_name = 'Admin access'
        verbose_name_plural = 'Admin accesses'

    def __str__(self):
        return self.key
