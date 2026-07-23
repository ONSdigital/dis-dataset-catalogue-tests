Feature: DCM Edition

    Scenario: User creates a new edition for a dataset series
        Given the user navigates to the DCM homepage
        When the user clicks on the Dataset catalogue link
        And the user clicks on the Create new series button
        And the user fills in the generated Series ID
        And the user fills in the generated Title
        And the user fills in "This is a smoke test dataset" as the Description
        And the user expands the "Business, industry and trade" topic
        And the user selects the "Business" subtopic
        And the user fills in "To be announced" as the Next release
        And the user fills in "smoke, test" as the Keywords
        And the user fills in "Test User" as the contact Name
        And the user fills in "test@ons.gov.uk" as the contact Email
        And the user clicks Add contact
        And the user clicks Create dataset series
        And the user clicks on the Create new edition button
        And the user fills in the generated Edition ID
        And the user fills in the generated Edition title
        And the user fills in "20" as the Day
        And the user fills in "07" as the Month
        And the user fills in "2026" as the Year
        And the user fills in "09" as the Hours
        And the user fills in "30" as the Minutes
        And the user selects "No accreditation" as the Quality designation
        And the user uploads the test CSV file
        And the user clicks Create edition
        Then the edition should be created successfully