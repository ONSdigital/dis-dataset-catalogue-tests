Feature: Dataset API

  Scenario: List all datasets
    Given the dataset API is available
    When I request a list of datasets
    Then the response status code should be 200
    And the response should contain a list of items

  Scenario: Get a dataset by ID
    Given the dataset API is available
    When I request the dataset with ID "cpih01"
    Then the response status code should be 200
    And the response should contain the dataset with ID "cpih01"

  Scenario: Get editions for a dataset
    Given the dataset API is available
    When I request the editions for dataset with ID "cpih01"
    Then the response status code should be 200
    And the response should contain a list of items