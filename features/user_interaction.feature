Feature: User interaction with Bot

  User interaction with Bot should be
  intuitive and predictable

  Scenario: Conversation
    Given telegram bot
    When start_bot called
    Then process should spawn
    When 'user' called '/conv' method
    Then 'user' should receive message 'Hi, I'm a conversational bot, and you?'
    And 'user' responds with 'Pepe'
    Then 'user' should receive message 'Nice to meet you, Pepe'
