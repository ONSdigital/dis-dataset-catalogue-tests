from behave import given, then
from playwright.sync_api import expect

DCM_URL = "http://localhost:29400/data-admin"

@given("the user navigates to the DCM homepage")
def user_navigates_to_dcm_homepage(context):
    context.page.goto(DCM_URL)

@then("the Dataset Catalogue Manager heading is visible")
def dcm_heading_is_visible(context):
    expect(context.page.get_by_text("Dataset Catalogue Manager")).to_be_visible()

@then("the navigation links are visible")
def navigation_links_are_visible(context):
    expect(context.page.get_by_role("link", name="Dataset catalogue")).to_be_visible()