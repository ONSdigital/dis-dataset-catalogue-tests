Feature: Overview page

  Scenario: A user navigates to the overview page for a dataset with multiple editions
    Given the user navigates to the overview page for series "overview-multiple-editions" with "4" editions
    Then the editions should be listed on the page

  Scenario: A user navigating to an overview page containing a single edition is redirected to the latest version
    Given the user navigates to the overview page for "overview-single-edition"
    Then there is a response code of "302"
    And the user is redirected to the latest version page

  Scenario: A user navigating to an editions page containing a single edition is redirected to the latest version
    Given the user navigates to the editions page for "editions-single-edition"
    Then there is a response code of "302"
    And the user is redirected to the latest version page

  Scenario: A user navigating to an editions page containing multple editions
    Given the user navigates to the editions page for "editions-multiple-editions" with "3" editions
    Then there is a response code of "200"
    And the editions should be listed on the page
    And the user can click on one of the editions
    And the version details should be displayed on the page

  Scenario: A user navigating to a specific version
    Given the user navigates to the version page for "version-page" with edition "version-page" and version "1"
    Then there is a response code of "200"
    And the version details should be displayed on the page

  Scenario: A user navigating to a specific edition page is redirected to the latest version of that edition
    Given the user navigates to the edition page for "edition-page" with edition "edition-page"
    Then there is a response code of "302"
    And the user is redirected to the latest version page

  Scenario: A user navigating to the versions page is redirected to the latest version
    Given the user navigates to the versions page for "versions-page" with edition "versions-page"
    Then there is a response code of "302"
    And the user is redirected to the latest version page

  Scenario: A user navigates to a dataset using an incorrect topic slug
    Given the user navigates to the overview page for "overview-incorrect-topic-slug" using incorrect topic slug
    Then there is a response code of "302"
    And the user is redirected to the correct overview page

  Scenario: A user can get JSON data for a dataset
    Given the user navigates to the data page for "dataset-json"
    Then there is a response code of "200"
    And the response should contain the dataset details in JSON format

  Scenario: A user can get JSON data for a dataset edition
    Given the user navigates to the data page for the edition of "edition-json" and "edition-json"
    Then there is a response code of "200"
    And the response should contain the dataset edition details in JSON format

  Scenario: A user can get JSON data for a dataset version
    Given the user navigates to the data page for the version of "version-json" and "version-json"
    Then there is a response code of "200"
    And the response should contain the version details in JSON format

  Scenario: A user can approve a version and see the updated state on the overview page
    Given the user navigates to the version page for "version-page" with edition "version-page" and version "1"
    When the user clicks the approve button
    Then the version page should show approved