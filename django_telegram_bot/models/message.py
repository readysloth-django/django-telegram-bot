from uuid import uuid4
from django.db import models

from .user import User


class Message(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4)

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
