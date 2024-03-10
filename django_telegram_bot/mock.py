from factory import LazyFunction, SubFactory
from factory.django import DjangoModelFactory
from mimesis.random import Random
from mimesis import (Person,
                     Text,
                     Datetime,
                     Numeric)

from .models import (Bot,
                     AdminAccess,
                     User,
                     Message)


RANDOM = Random()
PERSON = Person()
DATETIME = Datetime()
TEXT = Text()
NUMERIC = Numeric()


def random_token():
    return RANDOM.generate_string_by_mask(
        '######:@@@-@@@####@@@@@-@@@##@#@#@###@@##'
    )


class BotFactory(DjangoModelFactory):
    class Meta:
        model = Bot

    token = LazyFunction(random_token)


class AdminAccessFactory(DjangoModelFactory):
    class Meta:
        model = AdminAccess


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    telegram_id = LazyFunction(lambda: NUMERIC.integer_number(start=1))
    first_name = LazyFunction(PERSON.first_name)
    last_name = LazyFunction(PERSON.last_name)
    username = LazyFunction(PERSON.username)
    phone = LazyFunction(PERSON.phone_number)


class MessageFactory(DjangoModelFactory):
    class Meta:
        model = Message

    user = SubFactory(UserFactory)
    date = LazyFunction(DATETIME.datetime)
    text = LazyFunction(TEXT.sentence)
