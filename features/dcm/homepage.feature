Feature: DCM Homepage

    Scenario: View the DCM homepage
        Given the user navigates to the DCM homepage
        Then the Dataset Catalogue Manager heading is visible
        And the navigation links are visible