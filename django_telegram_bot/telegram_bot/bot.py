import os
import asyncio
import logging
import functools as ft
import multiprocessing as mp

from typing import (Optional,
                    Callable,
                    Coroutine,
                    Set)

from telegram import Bot
from telegram.ext import (Application,
                          ApplicationBuilder)

from django_telegram_bot.models import Bot as DBBot


BotTask = Callable[[Application], Coroutine]
AppBuilder = Callable[[str, Set[BotTask]], None]


class TelegramBot:
    def __init__(self,
                 token: str,
                 app_builder: Optional[AppBuilder] = None,
                 periodic_tasks: Set[BotTask] = None):
        self.token = token
        self.process = None
        self.app_builder = app_builder or self.build
        self.app_tasks = periodic_tasks or []

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

        for task in app_tasks:
            task(app)

        for func, args in app_args.items():
            builder = getattr(builder, func)(args)
        app.run_polling()


class DBTelegramBot(TelegramBot):
    def __init__(self, *args, **kwargs):
        super().__init__(DBBot.objects.get().token, *args, **kwargs)


def oneshot_task(func: Coroutine):
    @ft.wraps(func)
    def wrapper(app: Application):
        loop = asyncio.get_event_loop()
        loop.create_task(func(app.bot))
    return wrapper


def periodic_task(sleep_time: int):
    def decorator(func: Coroutine):
        @ft.wraps(func)
        def wrapper(app: Application):
            async def periodic_func():
                while True:
                    await func(app.bot)
                    await asyncio.sleep(sleep_time)
            loop = asyncio.get_event_loop()
            loop.create_task(periodic_func(app.bot))
        return wrapper
    return decorator
