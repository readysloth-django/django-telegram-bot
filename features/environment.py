import os
import subprocess as sp

from pathlib import Path


BEHAVE_FOLDER = Path('.') / Path('features')
MITMMOCK_FLOWS = BEHAVE_FOLDER / Path('flows')
MITMMOCK_REPLAY_SCRIPT = BEHAVE_FOLDER / Path('mitmmock_replay.py')

MITMMOCK_ARGS = ['poetry', 'run', 'mitmdump',
                 '--set', 'connection_strategy=lazy',
                 '--scripts', str(MITMMOCK_REPLAY_SCRIPT)]


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
    os.environ['http_proxy'] = 'http://127.0.0.1:8080'
    os.environ['https_proxy'] = 'https://127.0.0.1:8080'
    if 'SSL_CERT_FILE' not in os.environ:
        os.environ['SSL_CERT_FILE'] = '/usr/local/share/ca-certificates/mitmproxy.crt'


def after_scenario(context, scenario):
    context.mitmmock.terminate()
