from behave import given, when, then


@then("programmer-defined {task_type} broadcast tasks should execute")
def step_impl(context, task_type):
    if task_type == 'oneshot':
        message = 'ATTENTION, ATTENTION, THIS IS TEST BROADCAST'
        assert len([True for r in context.mitmmock_responses if message in r.content.decode()]) == 1
    if task_type == 'periodic':
        message = 'ATTENTION, ATTENTION, THIS IS PERIODIC TEST BROADCAST'
        assert len([True for r in context.mitmmock_responses if message in r.content.decode()]) > 1
