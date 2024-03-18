from behave import given, when, then

from django_telegram_bot.telegram_bot import TelegramBot


@when("'{user}' called '{method}' method")
def step_impl(context, user, method):
    assert any(user in r.content.decode() and method in r.content.decode()
               for r in context.mitmmock_responses)


@then("'{user}' should receive message '{message}'")
def step_impl(context, user, message):
    assert any(user in r.content.decode() and message in r.content.decode()
               for r in context.mitmmock_responses)


@then("'{user}' responds with '{message}'")
def step_impl(context, user, message):
    assert any(user in r.content.decode() and message in r.content.decode()
               for r in context.mitmmock_responses)
