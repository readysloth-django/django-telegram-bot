Feature: Telegram bot broadcast messages

  Telegram bot should correctly broadcast programmer-defined and
  user-defined messages to all chosen users

  Scenario: Broadcast once
    Given telegram bot
    When start_bot called
    Then process should spawn
    Then programmer-defined oneshot broadcast tasks should execute


  Scenario: Broadcast periodic
    Given telegram bot
    When start_bot called
    Then process should spawn
    Then programmer-defined periodic broadcast tasks should execute
