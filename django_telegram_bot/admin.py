from django.contrib import admin

from solo.admin import SingletonModelAdmin
from django_object_actions import DjangoObjectActions, action

from django_telegram_bot.models import (Bot,
                                        AdminAccess,
                                        User,
                                        Message,
                                        BotInteraction)

from django_telegram_bot.telegram_bot import DBTelegramBot


class DBTelegramBotAdmin(DjangoObjectActions, SingletonModelAdmin):
    @action(label='Start',
            description='Start bot',
            attrs={'class': 'btn btn-success form-control'})
    def toggle(self, request, obj):
        bot = DBTelegramBot.instance()
        if bot.is_running():
            bot.stop_bot()
            DBTelegramBotAdmin.start_stop.label = 'Start'
            DBTelegramBotAdmin.start_stop.description = 'Start bot'
            DBTelegramBotAdmin.start_stop.attrs = {'class': 'btn btn-success form-control'}
            return
        bot.start_bot()
        DBTelegramBotAdmin.toggle.label = 'Stop'
        DBTelegramBotAdmin.toggle.description = 'Stop bot'
        DBTelegramBotAdmin.toggle.attrs = {'class': 'btn btn-danger form-control'}

    change_actions = ['toggle']


admin.site.register(Bot, DBTelegramBotAdmin)


class AdminAccessAdmin(DjangoObjectActions, SingletonModelAdmin):
    @action(label='Regenerate',
            description='Regenerate key',
            attrs={'class': 'btn btn-success form-control'})
    def regeneration(self, request, obj):
        AdminAccess.objects.get().delete()
        AdminAccess.objects.create()

    change_actions = ['regeneration']


admin.site.register(AdminAccess, AdminAccessAdmin)


class UserAdmin(admin.ModelAdmin):
    readonly_fields = [
        'telegram_id',
        'first_name',
        'last_name',
        'username',
        'phone',
        'is_premium'
    ]


admin.site.register(User, UserAdmin)


class BotInteractionAdmin(admin.ModelAdmin):
    readonly_fields = [
        'user',
        'date',
        'data'
    ]


admin.site.register(BotInteraction, BotInteractionAdmin)


class MessageAdmin(admin.ModelAdmin):
    readonly_fields = [
        'message_id',
        'user',
        'date',
        'text',
        'reply'
    ]


admin.site.register(Message, MessageAdmin)
