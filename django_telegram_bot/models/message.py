from datetime import datetime
from uuid import uuid4

from django.db import models
from django.utils.translation import gettext_lazy as _

from .user import User


class BotInteraction(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4)

    user = models.ForeignKey(User,
                             on_delete=models.SET_NULL,
                             null=True)
    date = models.DateTimeField(_('Date'), default=datetime.now)
    data = models.JSONField(blank=True, null=True)

    class Meta:
        verbose_name = _('Bot interaction')
        verbose_name_plural = _('Bot interactions')

    def __str__(self):
        return f'{self.date}: {self.user}'


class Message(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4)

    message_id = models.IntegerField()
    user = models.ForeignKey(User,
                             on_delete=models.SET_NULL,
                             null=True)
    date = models.DateTimeField(_('Date'))
    text = models.TextField(_('Text'))
    reply = models.ForeignKey('Message',
                              on_delete=models.SET_NULL,
                              null=True)

    class Meta:
        verbose_name = _('Message')
        verbose_name_plural = _('Messages')

    def __str__(self):
        msg_text = self.text
        if len(msg_text) > 40:
            msg_text = f'{msg_text[:40]}...'
        return f'{self.date}: {msg_text}'
