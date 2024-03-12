from behave import given, when, then

from django_telegram_bot.telegram_bot import TelegramBot


@given('bot is running')
def step_impl(context):
    context.bot = TelegramBot('TOKEN')
    context.bot.start_bot()
    assert context.bot.is_running()


@when('stop_bot called')
def step_impl(context):
    context.bot.stop_bot()


@then('bot process should be terminated')
def step_impl(context):
    assert not context.bot.process


@then('is_running should return \'False\'')
def step_impl(context):
    assert not context.bot.is_running()
