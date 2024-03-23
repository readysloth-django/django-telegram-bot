from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DjangoTelegramBotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'django_telegram_bot'
    verbose_name = _('Telegram bot control')
