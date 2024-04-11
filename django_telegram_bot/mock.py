from factory import LazyFunction, SubFactory
from factory.django import DjangoModelFactory
from mimesis.random import Random
from mimesis import (Person,
                     Text,
                     Datetime,
                     Numeric,
                     Development)

from .models import (Bot,
                     AdminAccess,
                     User,
                     Message,
                     BotInteraction)


RANDOM = Random()
PERSON = Person()
DATETIME = Datetime()
TEXT = Text()
NUMERIC = Numeric()
DEVELOPMENT = Development()


def random_token():
    return RANDOM.generate_string_by_mask(
        '######:@@@-@@@####@@@@@-@@@##@#@#@###@@##'
    )


class BotFactory(DjangoModelFactory):
    class Meta:
        model = Bot

    token = LazyFunction(random_token)

    create = BotFactory.objects.get_or_create


class AdminAccessFactory(DjangoModelFactory):
    class Meta:
        model = AdminAccess

    create = AdminAccess.objects.get_or_create


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    telegram_id = LazyFunction(lambda: NUMERIC.integer_number(start=1))
    first_name = LazyFunction(PERSON.first_name)
    last_name = LazyFunction(PERSON.last_name)
    username = LazyFunction(PERSON.username)
    phone = LazyFunction(PERSON.phone_number)
    is_premium = LazyFunction(DEVELOPMENT.boolean)


class BotInteractionFactory(DjangoModelFactory):
    class Meta:
        model = BotInteraction

    user = SubFactory(UserFactory)
    date = LazyFunction(DATETIME.datetime)
    data = {}


class MessageFactory(DjangoModelFactory):
    class Meta:
        model = Message

    message_id = LazyFunction(lambda: NUMERIC.integer_number(start=1))
    user = SubFactory(UserFactory)
    date = LazyFunction(DATETIME.datetime)
    text = LazyFunction(TEXT.sentence)
    reply = None
