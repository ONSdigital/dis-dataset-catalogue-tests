Feature: DCM Version

    Scenario: User creates a new version for a dataset edition
        Given the user navigates to the series detail page for "static-test-dataset"
        When the user clicks on the "This is an edition title for version 2" edition
        And the user clicks on the Create new version button
        And the user fills in "21" as the "Day"
        And the user fills in "07" as the "Month"
        And the user fills in "2026" as the "Year"
        And the user fills in "09" as the "Hours"
        And the user fills in "30" as the "Minutes"
        And the user selects "No accreditation" as the Quality designation
        And the user uploads the test CSV file
        And the user clicks Create version
        Then the version should be created successfully