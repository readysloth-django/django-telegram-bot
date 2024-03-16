from django.db import models

from phonenumber_field.modelfields import PhoneNumberField


class User(models.Model):
    telegram_id = models.IntegerField('telegram id', primary_key=True)
    first_name = models.CharField('First name', max_length=128)
    last_name = models.CharField('Last name', max_length=128, null=True)
    username = models.CharField('Username', max_length=128, null=True)
    phone = PhoneNumberField('Phone Number', null=True)

    is_premium = models.BooleanField('Premium', default=False)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        representation = f'@{self.username} {self.first_name}'
        if self.last_name:
            representation += f' {self.last_name}'
        if self.is_premium:
            representation = '*Premium* ' + representation
        return representation
