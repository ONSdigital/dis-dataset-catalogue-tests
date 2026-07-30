from datetime import datetime

from behave import given, then, when
from playwright.sync_api import expect

SERIES_URL = "http://localhost:29400/data-admin/series"


@given('the user navigates to the series detail page for "{series_id}"')
def user_navigates_to_series_detail_page(context, series_id):
    context.page.goto(f"{SERIES_URL}/{series_id}")
    context.page.wait_for_load_state("networkidle")


@when("the user clicks on the Create new edition button")
def user_clicks_create_new_edition(context):
    context.page.get_by_role("button", name="Create new edition").click()
    context.page.wait_for_url("**/editions/create")
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    context.edition_id = f"time-series-{timestamp}"
    context.edition_title = f"Time Series {timestamp}"


@when("the user fills in the generated Edition ID")
def user_fills_in_generated_edition_id(context):
    context.page.get_by_label("Edition ID").fill(context.edition_id)


@when("the user fills in the generated Edition title")
def user_fills_in_generated_edition_title(context):
    context.page.get_by_label("Edition title").fill(context.edition_title)


@when("the user uploads the test CSV file")
def user_uploads_test_csv_file(context):
    file_input = context.page.get_by_test_id("dataset-upload-input")
    file_input.set_input_files(context.test_csv_path)
    file_input.dispatch_event("change")
    context.page.wait_for_timeout(2000)


@when("the user clicks Create edition")
def user_clicks_create_edition(context):
    context.page.get_by_role("button", name="Create edition").click()
    context.page.wait_for_url("**/editions/**")


@then("the edition should be created successfully")
def edition_should_be_created_successfully(context):
    expect(context.page.get_by_text("Edition saved.")).to_be_visible()
    expect(context.page.get_by_role("heading", name=context.edition_title)).to_be_visible()