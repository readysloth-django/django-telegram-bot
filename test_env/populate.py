#!/bin/env python3

import os
import inspect
import argparse

os.environ['DJANGO_SETTINGS_MODULE'] = 'django_telegram_bot_test.settings'

import django
django.setup()

from django_telegram_bot import mock

FACTORIES = {name.replace('Factory', ''): entity
             for name, entity in inspect.getmembers(mock)
             if name.endswith('Factory')
             and name not in ['DjangoModelFactory', 'SubFactory']}


parser = argparse.ArgumentParser(description='DB population tool')
parser.add_argument('-n', '--count',
                    default=1,
                    type=int,
                    help='amount of entities to add')
parser.add_argument('-a', '--all',
                    action='store_true',
                    help='add all types to DB (ignores entity)')
parser.add_argument('--entity',
                    choices=FACTORIES.keys(),
                    default=[],
                    nargs='+',
                    help='entities to add')

args = parser.parse_args()

if args.all:
    for entity in FACTORIES:
        print(f'Adding {entity}')
        for _ in range(args.count):
            FACTORIES[entity]()
    exit(0)

for entity in args.entity:
    for _ in range(args.count):
        FACTORIES[entity]()
