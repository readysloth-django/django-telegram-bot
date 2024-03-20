from datetime import datetime
from uuid import uuid4
from django.db import models

from .user import User


class BotInteraction(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4)

    user = models.ForeignKey(User,
                             on_delete=models.SET_NULL,
                             null=True)
    date = models.DateTimeField('Date', default=datetime.now)
    data = models.JSONField(blank=True, null=True)

    class Meta:
        verbose_name = 'Bot interaction'
        verbose_name_plural = 'Bot interactions'

    def __str__(self):
        return f'{self.date}: {self.user}'


class Message(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4)

    message_id = models.IntegerField()
    user = models.ForeignKey(User,
                             on_delete=models.SET_NULL,
                             null=True)
    date = models.DateTimeField('Date')
    text = models.TextField('Text')
    reply = models.ForeignKey('Message',
                              on_delete=models.SET_NULL,
                              null=True)

    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'

    def __str__(self):
        msg_text = self.text
        if len(msg_text) > 40:
            msg_text = f'{msg_text[:40]}...'
        return f'{self.date}: {msg_text}'
