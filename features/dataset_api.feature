Feature: Dataset API

  Scenario: List all datasets
    Given the dataset API is available
    When I request a list of datasets
    Then the response status code should be "200"
    And the response should contain a list of items

  Scenario: Get a dataset by ID
    Given the dataset API is available
    When I request the dataset with ID "dataset-to-get"
    Then the response status code should be "200"
    And the response should contain the requested dataset

  Scenario: Get editions for a dataset
    Given the dataset API is available
    When I request the editions for dataset with ID "dataset-to-get"
    Then the response status code should be "200"
    And the response should contain a list of items

  Scenario: Get an edition by ID
    Given the dataset API is available
    When I request the edition with ID "edition-to-get" for dataset with ID "dataset-get-edition"
    Then the response status code should be "200"
    And the response should contain the requested edition

  Scenario: Get versions for a dataset edition
    Given the dataset API is available
    When I request the versions for edition ID "edition-get-versions" and dataset ID "dataset-get-versions"
    Then the response status code should be "200"
    And the response should contain a list of items

  Scenario: Get a version by ID
    Given the dataset API is available
    When I request version "1" for edition ID "edition-get-version" and dataset ID "dataset-get-version"
    Then the response status code should be "200"
    And the response should contain the version with ID "1"

  Scenario: Get metadata for a version
    Given the dataset API is available
    When I request the metadata for dataset ID "dataset-get-metadata", edition ID "edition-get-metadata", version "1"
    Then the response status code should be "200"
    And the response should contain the metadata for version "1"

  Scenario: Get dimensions for a version - filterable/cantabular only
    Given the dataset API is available
    When I request the dimensions for dataset ID "cpih01", edition ID "time-series", version "1"
    Then the response status code should be "200"
    And the response should contain the dimensions for the requested version

  Scenario: Get options for a dimension - filterable/cantabular only
    Given the dataset API is available
    When I request the options for dataset ID "cpih01", edition ID "time-series", version "1", dimension "geography"
    Then the response status code should be "200"
    And the response should contain the options for dimension "geography"

  Scenario: Add a dataset
    Given the dataset API is available
    When I add a new dataset with ID "dataset-to-add"
    Then the response status code should be "201"
    And the response should contain the requested dataset

  Scenario: Update a dataset by ID
    Given the dataset API is available
    When I update the dataset "dataset-to-update" with title "Changed dataset title"
    Then the response status code should be "200"
    And the response should include the updated dataset title "Changed dataset title"

  Scenario: Delete a dataset by ID
    Given the dataset API is available
    When I delete the dataset "dataset-to-delete"
    Then the response status code should be "204"

  Scenario: Add a version no ID
    Given the dataset API is available
    When I add a new version for dataset ID "dataset-add-version" and edition ID "edition-add-version"
    Then the response status code should be "201"
    And the response should contain the version with ID "1"

  Scenario: Add a version by ID
    Given the dataset API is available
    When I add a new version for dataset ID "dataset-add-version", edition ID "edition-add-version" and version "1"
    Then the response status code should be "201"
    And the response should contain the version with ID "1"

  Scenario: Update a version
    Given the dataset API is available
    When I update version "1" for dataset ID "dataset-update-version", edition ID "edition-update-version"
    Then the response status code should be "200"
    And the response should include the updated edition title "New edition title"

  Scenario: Update state of a version
    Given the dataset API is available
    When I update the state to "approved" for version "1" for dataset ID "dataset-update-state", edition ID "edition-update-state"
    Then the response status code should be "200"
    And the response should contain the version with state "approved"


  Scenario: Delete a version by ID
    Given the dataset API is available
    When I delete version "1" for dataset ID "dataset-delete-version", edition ID "edition-delete-version"
    Then the response status code should be "204"
