# Created by Tymoteusz Paul at 18/01/2016

# Changes to setup tests that need input data
Feature: ServiceRegistry

  Background:
    Given there is an empty ServiceRegistry

  Scenario Outline: Add service
    When I add a service "<service>" with version "<version>"
    Then I should be notified with a change "<change>"
    Examples:
      | service | version | change  |
      | test    | 0.0.1   | created |
      | test    | 0.0.1   | created |
      | test    | 0.0.2   | created |
      | test    | 0.0.2   | created |
      | test2   | 0.0.2   | created |
      | test2   | 0.0.2   | created |


  @find_service
  Scenario Outline: Find service:
    Given a set of specific services:
      | service | version |
      | test    | 0.0.1   |
      | test    | 0.0.1   |
      | test    | 0.0.2   |
      | test    | 0.0.2   |
      | test2   | 0.0.2   |
      | test2   | 0.0.2   |
    When I search for a service "<service>" with version "<version>"
    Then I should find count "<count>" instances of service
    And the service "<service>" should have the correct type
    And the service "<service>" should have the correct version "<version>"
    Examples:
      | service | version | count |
      | test    | 0.0.1   |   2   |
      | test    | 0.0.2   |   2   |
      | test2   | 0.0.2   |   2   |


  @find_non_existing_service
  Scenario Outline: Finding non existing service:
    When I search for a service "<service>" with version "<version>"
    Then I should find count "<count>" services
    Examples:
      | service | version | count |
      | test    | 0.0.4   |   0   |
      | test3   | 0.0.1   |   0   |

  Scenario Outline: Finding service without version:
    Given a set of specific services:
      | service | version |
      | test    | 0.0.1   |
      | test    | 0.0.1   |
      | test    | 0.0.2   |
      | test    | 0.0.2   |
      | test2   | 0.0.2   |
      | test2   | 0.0.2   |
    When I search for a service "<service>" without version
    Then I should find count "<count>" services
    And the service "<service>" should have the correct type
    Examples:
      | service | count |
      | test    |   4   |
      | test2   |   2   |

  Scenario Outline: updating a service:
    Given a set of specific services:
      | service | version |
      | test    | 0.0.1   |
    When I update a service
    Then I should be notified with a change "<change>"
    Examples:
      | change  |
      | changed |

  Scenario Outline: Removing a service:
    Given a set of specific services:
      | service | version |
      | test    | 0.0.1   |
    When I remove a service
    Then the service should be removed
    And I should be notified with a change "<change>"
    Examples:
      | service | change |
      | test    | removed|
