import os
import time
import pickle
import base64
import subprocess as sp

from pathlib import Path
from threading import Thread

from mitmproxy.http import Request, Response
from django_telegram_bot.mock import BotFactory


BEHAVE_FOLDER = Path('.') / Path('features')
MITMMOCK_FLOWS = BEHAVE_FOLDER / Path('flows')
MITMMOCK_REPLAY_SCRIPT = BEHAVE_FOLDER / Path('mitmmock_replay.py')

MITMMOCK_ARGS = ['poetry', 'run', 'mitmdump',
                 '--set', 'connection_strategy=lazy',
                 '--scripts', str(MITMMOCK_REPLAY_SCRIPT)]


def before_step(context, scenario):
    # ensures all multiprocessing, multithreading and request handling
    # would finish in background
    time.sleep(0.5)


def before_scenario(context, scenario):
    scenario_flow = MITMMOCK_FLOWS / Path(scenario.name)
    args = MITMMOCK_ARGS + ['--set', f'mitmmock_dump={scenario_flow}.mitmmock']
    env = dict(os.environ)
    env['DJANGO_TG_BOT'] = Path(".").resolve()
    context.mitmmock = sp.Popen(args,
                                env=env,
                                stderr=sp.PIPE,
                                stdout=sp.PIPE,
                                universal_newlines=True)
    for line in context.mitmmock.stderr:
        if 'mitmmock running' in line:
            break

    context.mitmmock_requests = []
    context.mitmmock_responses = []

    def flow_consumer():
        for line in context.mitmmock.stderr:
            pickled_data = base64.b64decode(line.strip())
            unpickled_obj = pickle.loads(pickled_data)
            if type(unpickled_obj) == Request:
                context.mitmmock_requests.append(unpickled_obj)
            elif type(unpickled_obj) == Response:
                context.mitmmock_responses.append(unpickled_obj)

    Thread(target=flow_consumer, daemon=True).start()

    if context.mitmmock.poll() is not None:
        raise RuntimeError(''.join(context.mitmmock.stdout.readlines()))

    os.environ['http_proxy'] = 'http://127.0.0.1:8080'
    os.environ['https_proxy'] = 'https://127.0.0.1:8080'
    if 'SSL_CERT_FILE' not in os.environ:
        os.environ['SSL_CERT_FILE'] = '/usr/local/share/ca-certificates/mitmproxy.crt'
    bot = BotFactory.create()
    context.token = bot.token


def after_scenario(context, scenario):
    context.mitmmock.terminate()
    if hasattr(context, 'bot'):
        if context.bot.process:
            context.bot.process.terminate()
