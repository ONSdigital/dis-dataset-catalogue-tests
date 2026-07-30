from behave import given, then, when
from playwright.sync_api import expect

SERIES_URL = "http://localhost:29400/data-admin/series"


@given('the user navigates to the edition page for "{series_id}" and "{edition_id}"')
def user_navigates_to_edition_page(context, series_id, edition_id):
    context.page.goto(f"{SERIES_URL}/{series_id}/editions/{edition_id}")
    context.page.wait_for_load_state("networkidle")

@when('the user clicks on the "{edition_title}" edition')
def user_clicks_on_edition(context, edition_title):
    context.page.get_by_role("link", name=edition_title).click()
    context.page.wait_for_load_state("networkidle")

@when("the user clicks on the Create new version button")
def user_clicks_create_new_version(context):
    context.page.get_by_role("button", name="Create new version").click()
    context.page.wait_for_url("**/versions/create**")

@when("the user clicks Create version")
def user_clicks_create_version(context):
    context.page.get_by_role("button", name="Create version").click()
    context.page.wait_for_url("**/versions/**")


@then("the version should be created successfully")
def version_should_be_created_successfully(context):
    expect(context.page.get_by_text("Version saved.")).to_be_visible()

