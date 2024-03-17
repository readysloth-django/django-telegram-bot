from behave import given, when, then

from django_telegram_bot.telegram_bot import TelegramBot, DBTelegramBot


@given('telegram bot with token stored in DB')
def step_impl(context):
    context.bot = DBTelegramBot()


@given('telegram bot')
def step_impl(context):
    context.bot = TelegramBot(context.token)


@when('start_bot called')
def step_impl(context):
    context.bot.start_bot()


@then('process should spawn')
def step_impl(context):
    assert context.bot.process


@then("request '{url}' url")
def step_impl(context, url):
    concrete_token = url.replace('TOKEN', context.token)
    assert any(concrete_token in r.url for r in context.mitmmock_requests)


@then('is_running should return \'True\'')
def step_impl(context):
    assert context.bot.is_running()
