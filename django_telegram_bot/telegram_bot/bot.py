import os
import asyncio
import logging
import functools as ft
import multiprocessing as mp

from threading import Thread
from typing import (Optional,
                    Callable,
                    Coroutine,
                    Set)

from telegram import Bot
from telegram.ext import (BaseHandler,
                          Application,
                          ApplicationBuilder)

from django_telegram_bot.models import (User,
                                        Message,
                                        BotInteraction,
                                        Bot as DBBot)


BotTask = Callable[[Application], Coroutine]
AppBuilder = Callable[[str, Set[BotTask]], None]


class AddToDBHandler(BaseHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(self.do_nothing, *args, **kwargs)

    async def do_nothing(self, *args, **kwargs):
        pass

    def check_update(self, update):
        def db_update():
            user = update.effective_user
            user_db_obj = None
            if user:
                user_db_obj, _ = User.objects.get_or_create(
                    telegram_id=user.id,
                    first_name=user.first_name,
                    last_name=user.last_name,
                    username=user.username,
                    is_premium=bool(user.is_premium)
                )

            message = update.effective_message
            message_db_obj = None
            if (message and
                    user_db_obj and
                    message.from_user and
                    message.from_user.id == user_db_obj.telegram_id):
                message_db_obj = Message.objects.create(
                    message_id=message.message_id,
                    user=user_db_obj,
                    date=message.date,
                    text=message.text
                )
                reply = message.reply_to_message
                if reply:
                    user_tg_id = None
                    if reply.from_user:
                        user_tg_id = reply.from_user.id
                    original_db_message = Message.objects.filter(
                        message_id=reply.message_id,
                        user__telegram_id=user_tg_id
                    ).first()
                    original_db_message.reply = message_db_obj
                    original_db_message.save()

            BotInteraction.objects.create(user=user_db_obj, data=update.to_dict())

        db_update_thread = Thread(target=db_update)
        db_update_thread.start()
        db_update_thread.join()
        return False


class TelegramBot:
    def __init__(self,
                 token: str,
                 app_builder: Optional[AppBuilder] = None,
                 periodic_tasks: Set[BotTask] = None):
        self.token = token
        self.process = None
        self.app_builder = app_builder or self.build
        self.app_tasks = periodic_tasks or set()

    def start_bot(self, **kwargs):
        if self.process:
            self.stop_bot()
        logging.debug(f'Creating bot process for {self.token}')
        self.process = mp.Process(target=self.app_builder,
                                  args=[self.token, self.app_tasks],
                                  kwargs=kwargs)
        logging.debug(f'Starting bot process for {self.token}')
        self.process.start()

    def stop_bot(self):
        if not self.process:
            logging.warning('Bot process is not yet started!')
            return
        logging.info('Terminating bot process')
        self.process.terminate()
        self.process = None

    def is_running(self):
        return self.process and self.process.is_alive()

    @staticmethod
    def build(token: str,
              app_tasks: Set[BotTask],
              **kwargs):
        if not token:
            token = os.getenv('TELEGRAM_TOKEN')
        app_args = {}
        if 'app' in kwargs:
            app_args = kwargs['app']

        builder_args = kwargs
        if 'builder' in kwargs:
            builder_args = kwargs['builder']

        builder = ApplicationBuilder().token(token)
        for func, args in builder_args.items():
            builder = getattr(builder, func)(args)
        app = builder.build()
        app.add_handler(AddToDBHandler())

        for task in app_tasks:
            task(app)

        for func, args in app_args.items():
            builder = getattr(builder, func)(args)
        app.run_polling()


class DBTelegramBot(TelegramBot):
    def __init__(self, *args, **kwargs):
        super().__init__(DBBot.objects.get().token, *args, **kwargs)

    @classmethod
    def instance(cls, *args, **kwargs):
        if not hasattr(cls, 'bot_instance'):
            cls.bot_instance = DBTelegramBot(*args, **kwargs)
        return cls.bot_instance


async def wait_for_app(app: Application,
                       task: Coroutine,
                       supply_app: bool = False):
    while not app.running:
        await asyncio.sleep(0.5)
    loop = asyncio.get_event_loop()
    if supply_app:
        loop.create_task(task(app))
    else:
        loop.create_task(task(app.bot))


def oneshot_task(*args, **kwargs):
    def decorator(func: Coroutine):
        @ft.wraps(func)
        def wrapper(app: Application):
            loop = asyncio.get_event_loop()
            loop.create_task(wait_for_app(app, func, *args, **kwargs))
        return wrapper
    return decorator


def periodic_task(sleep_time: int, *args, supply_app: bool = False, **kwargs):
    def decorator(func: Coroutine):
        @ft.wraps(func)
        def wrapper(app: Application):
            async def periodic_func(*args, **kwargs):
                while True:
                    if supply_app:
                        await func(app)
                    else:
                        await func(app.bot)
                    await asyncio.sleep(sleep_time)
            loop = asyncio.get_event_loop()
            loop.create_task(wait_for_app(app, periodic_func, *args, **kwargs))
        return wrapper
    return decorator
