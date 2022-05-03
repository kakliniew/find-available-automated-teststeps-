Feature: Is it Friday yet?
  Everybody wants to know when it's Friday

	@Tag12
  Scenario: Sunday isn't Friday
    Given today is Sunday
    When I find whether it's Friday yet
    Then I should be told "Nope"

	@TAG
  Scenario: Friday is Friday
    Given today is not Friday
    When I ask whether it's Friday yet
    Then I should noticed "TGIF"
    Then I search noticed "TGIF"
    Then She searches noticed "TGIF"