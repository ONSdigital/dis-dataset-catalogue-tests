Feature: DCM Series

    Scenario: User can find a dataset and version
        Given the user navigates to the DCM homepage
        When the user clicks on the Dataset catalogue link
        Then the series list page should be visible
        And the "Consumer price inflation tables" dataset should be listed

    Scenario: User can search for a dataset by ID
        Given the user navigates to the DCM homepage
        When the user clicks on the Dataset catalogue link
        And the user searches for "static-test-dataset" in the search box
        Then a dataset with the Series ID "static-test-dataset" should be visible
        And the "Consumer price inflation tables" dataset should be listed

    Scenario: User searches for a dataset with an invalid ID
        Given the user navigates to the DCM homepage
        When the user clicks on the Dataset catalogue link
        And the user searches for "invalid-dataset-id" in the search box
        Then no results should be found for "invalid-dataset-id"

    Scenario: User creates a new dataset series
        Given the user navigates to the DCM homepage
        When the user clicks on the Dataset catalogue link
        And the user clicks on the Create new series button
        And the user fills in the generated Series ID
        And the user fills in the generated Title
        And the user fills in "This is a smoke test dataset" as the "Description"
        And the user expands the "Business, industry and trade" topic
        And the user selects the "Business" subtopic
        And the user fills in "To be announced" as the "Next release"
        And the user fills in "smoke, test" as the "Keywords"
        And the user fills in "Test User" as the "Name"
        And the user fills in "test@ons.gov.uk" as the "Email"
        And the user clicks Add contact
        And the user clicks Create dataset series
        Then the generated dataset should be listed