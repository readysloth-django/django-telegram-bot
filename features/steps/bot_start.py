from behave import given, when, then

from django_telegram_bot.telegram_bot import TelegramBot


@given('telegram bot')
def step_impl(context):
    context.bot = TelegramBot('TOKEN')


@when('start_bot called')
def step_impl(context):
    context.bot.start_bot()


@then('process should spawn')
def step_impl(context):
    assert context.bot.process


@then("request '{url}' url")
def step_impl(context, url):
    assert url in context.mitmmock.stderr.readline()


@then('is_running should return \'True\'')
def step_impl(context):
    assert context.bot.is_running()
