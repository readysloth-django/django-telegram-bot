from django.db import models
from django.utils.translation import gettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField


class User(models.Model):
    telegram_id = models.IntegerField(_('telegram id'), primary_key=True)
    first_name = models.CharField(_('First name'), max_length=128)
    last_name = models.CharField(_('Last name'), max_length=128, null=True)
    username = models.CharField(_('Username'), max_length=128, null=True)
    phone = PhoneNumberField(_('Phone Number'), null=True)

    is_premium = models.BooleanField(_('Premium'), default=False)

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        representation = f'@{self.username} {self.first_name}'
        if self.last_name:
            representation += f' {self.last_name}'
        if self.is_premium:
            representation = '*Premium* ' + representation
        return representation
