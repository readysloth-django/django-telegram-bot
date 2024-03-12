Feature: Telegram bot control

  Telegram bot should be brought up and stopped
  via API calls easily.

  Scenario: Bot start
    Given telegram bot
    When start_bot called
    Then process should spawn
    And request '/botTOKEN/getMe' url
    And request '/botTOKEN/deleteWebhook' url
    And is_running should return 'True'

  Scenario: Bot stop
    Given bot is running
    When stop_bot called
    Then bot process should be terminated
    And is_running should return 'False'
