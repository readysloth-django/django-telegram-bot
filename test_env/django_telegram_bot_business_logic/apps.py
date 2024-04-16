import functools as ft

from django.apps import AppConfig
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import OperationalError, ProgrammingError

from threading import Thread


def small_conversation(app):
    from telegram.ext import (filters,
                              CommandHandler,
                              MessageHandler,
                              ConversationHandler)
    from django_telegram_bot.telegram_bot import Interaction

    async def response(update, context):
        return f'Nice to meet you, {update.message.text}'

    smalltalk = Interaction(
        'hello',
        "Hi, I'm a conversational bot, and you?",
        ft.partial(CommandHandler, 'conv'),
        next_interaction=Interaction(
            'response',
            response,
            ft.partial(MessageHandler, filters.TEXT)
        )
    )

    handler = ConversationHandler([smalltalk.handler], smalltalk.to_dict(), [])
    app.add_handler(handler)


def kbd_conversation(app):
    from telegram import InlineKeyboardButton, InlineKeyboardMarkup
    from telegram.ext import (filters,
                              CommandHandler,
                              CallbackQueryHandler,
                              ConversationHandler)
    from django_telegram_bot.telegram_bot import Interaction

    async def response(update, context):
        await update.callback_query.answer()
        return f'Your option is {update.callback_query.data}'

    async def keyboard(update, context):
        return [
            [InlineKeyboardButton('first option', callback_data='first')],
            [InlineKeyboardButton('second option', callback_data='second')],
            [InlineKeyboardButton('third option', callback_data='third')],
        ]

    callback_query_talk = Interaction(
        'hello',
        "Pick one of the options",
        ft.partial(CommandHandler, 'kbd'),
        keyboard=keyboard,
        markup=InlineKeyboardMarkup,
        next_interaction=Interaction(
            'response-kbd',
            response,
            CallbackQueryHandler
        )
    )

    handler = ConversationHandler([callback_query_talk.handler],
                                  callback_query_talk.to_dict(),
                                  [])
    app.add_handler(handler)


def simple_broadcast():
    from django_telegram_bot.telegram_bot.ext import simple_broadcast_task
    return simple_broadcast_task(
        'ATTENTION, ATTENTION, THIS IS TEST BROADCAST'
    )


def simple_periodic_broadcast():
    from django_telegram_bot.telegram_bot.ext import simple_periodic_broadcast_task
    return simple_periodic_broadcast_task(
        10,
        'ATTENTION, ATTENTION, THIS IS PERIODIC TEST BROADCAST'
    )


class DjangoTelegramBotBusinessLogicConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'django_telegram_bot_business_logic'

    def bot_init(self):
        try:
            from django_telegram_bot.telegram_bot import DBTelegramBot
            bot = DBTelegramBot.instance()
        except (OperationalError, ProgrammingError, ObjectDoesNotExist):
            return
        bot.app_tasks.add(small_conversation)
        bot.app_tasks.add(kbd_conversation)
        bot.app_tasks.add(simple_broadcast())
        bot.app_tasks.add(simple_periodic_broadcast())

    def ready(self):
        # Solely to get rid of django.core.exceptions.SynchronousOnlyOperation
        # in mitmmock running from `behave`
        bot_init_thread = Thread(target=self.bot_init, daemon=True)
        bot_init_thread.start()
