import logging

from typing import Callable

from django_telegram_bot.models import User

from telegram import Bot
from telegram.constants import ParseMode

from asgiref.sync import sync_to_async

from .bot import oneshot_task, periodic_task

UserPredicate = Callable[[User], bool]


def simple_broadcast_task(message: str,
                          user_predicate: UserPredicate = lambda *args, **kwargs: True):
    @oneshot_task
    async def task(bot: Bot):
        async for user in sync_to_async(User.objects.all)():
            try:
                if user_predicate(user):
                    await bot.send_message(user.telegram_id,
                                           message,
                                           parse_mode=ParseMode.HTML)
            except Exception:
                logging.exception(f'Attempt to send "{message}" to {user.telegram_id} failed')
                continue
    return task


def simple_periodic_task(sleep_time: int,
                         message: str,
                         user_predicate: UserPredicate = lambda *args, **kwargs: True):
    @periodic_task(sleep_time)
    async def task(bot: Bot):
        async for user in sync_to_async(User.objects.all)():
            try:
                if user_predicate(user):
                    await bot.send_message(user.telegram_id,
                                           message,
                                           parse_mode=ParseMode.HTML)
            except Exception:
                logging.exception(f'Attempt to send "{message}" to {user.telegram_id} failed')
                continue
    return task
