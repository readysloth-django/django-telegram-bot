import logging

from typing import Callable
from datetime import datetime

from django_telegram_bot.models import (User,
                                        BroadcastTask,
                                        ScheduledBroadcastTask,
                                        ScheduledPeriodicBroadcastTask)

from telegram import Bot
from telegram.constants import ParseMode

from asgiref.sync import sync_to_async

from .bot import oneshot_task, periodic_task

UserPredicate = Callable[[User], bool]


def simple_broadcast_task(message: str,
                          user_predicate: UserPredicate = lambda *args, **kwargs: True):
    @oneshot_task
    async def task(bot: Bot):
        async for user in User.objects.all():
            try:
                if user_predicate(user):
                    await bot.send_message(user.telegram_id,
                                           message,
                                           parse_mode=ParseMode.HTML)
            except Exception:
                logging.exception(f'Attempt to send "{message}" to {user.telegram_id} failed')
                continue
    return task


def simple_periodic_broadcast_task(sleep_time: int,
                                   message: str,
                                   user_predicate: UserPredicate = lambda *args, **kwargs: True):
    @periodic_task(sleep_time)
    async def task(bot: Bot):
        async for user in User.objects.all():
            try:
                if user_predicate(user):
                    await bot.send_message(user.telegram_id,
                                           message,
                                           parse_mode=ParseMode.HTML)
            except Exception:
                logging.exception(f'Attempt to send "{message}" to {user.telegram_id} failed')
                continue
    return task


def db_broadcast_tasks(sleep_time: int,
                       user_predicate: UserPredicate = lambda *args, **kwargs: True):
    @periodic_task(sleep_time)
    async def task(bot: Bot):
        bcast_filter = sync_to_async(BroadcastTask.objects.filter)
        async for task in bcast_filter(executed=False, parent_link=False):
            await simple_broadcast_task(task.text, user_predicate)(bot)
            task.executed = True
            await sync_to_async(task.save)()
    return task


def db_sched_broadcast_tasks(sleep_time: int,
                             user_predicate: UserPredicate = lambda *args, **kwargs: True):
    @periodic_task(sleep_time)
    async def task(bot: Bot):
        bcast_filter = sync_to_async(ScheduledBroadcastTask.objects.filter)
        async for task in bcast_filter(executed=False, parent_link=False):
            if task.date > datetime.now():
                continue
            await simple_broadcast_task(task.text, user_predicate)(bot)
            task.executed = True
            await sync_to_async(task.save)()
    return task


def db_sched_periodic_broadcast_tasks(sleep_time: int,
                                      user_predicate: UserPredicate = lambda *args, **kwargs: True):
    @periodic_task(sleep_time)
    async def task(bot: Bot):
        marked_for_cleanup = []
        bcast_filter = sync_to_async(ScheduledPeriodicBroadcastTask.objects.filter)
        bcast_sched_create = sync_to_async(ScheduledPeriodicBroadcastTask.objects.create)
        async for task in bcast_filter(executed=False):
            if task.date > datetime.now():
                continue
            await simple_broadcast_task(task.text, user_predicate)(bot)
            task.executed = True
            await sync_to_async(task.save)()
            marked_for_cleanup.append(task)

            await bcast_sched_create(
                text=task.text,
                time_delta=task.time_delta,
                date=task.date + task.time_delta
            )

        for task in marked_for_cleanup:
            await sync_to_async(task.delete)()
    return task
