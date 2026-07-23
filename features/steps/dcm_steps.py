from datetime import datetime

from behave import given, then, when
from playwright.sync_api import expect

DCM_URL = "http://localhost:29400/data-admin"


@given("the user navigates to the DCM homepage")
def user_navigates_to_dcm_homepage(context):
    context.page.goto(DCM_URL)

@when("the user clicks on the Dataset catalogue link")
def user_clicks_dataset_catalogue_link(context):
    context.page.goto("http://localhost:29400/data-admin/series")
    context.page.wait_for_load_state("networkidle")

@when("the user clicks on the Create new series button")
def user_clicks_create_new_series(context):
    context.page.get_by_role("button", name="Create new series").click()
    context.page.wait_for_url("**/series/create")
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    context.series_id = f"smoke-test-dataset-{timestamp}"
    context.series_title = f"Smoke Test Dataset {timestamp}"

@when("the user fills in the generated Series ID")
def user_fills_in_generated_series_id(context):
    context.page.get_by_label("Series ID").fill(context.series_id)

@when("the user fills in the generated Title")
def user_fills_in_generated_title(context):
    context.page.get_by_label("Title").fill(context.series_title)

@when('the user fills in "{value}" as the Description')
def user_fills_in_description(context, value):
    context.page.get_by_label("Description").fill(value)

@when('the user expands the "{topic}" topic')
def user_expands_topic(context, topic):
    context.page.get_by_role("button", name=topic).click()

@when('the user selects the "{subtopic}" subtopic')
def user_selects_subtopic(context, subtopic):
    context.page.get_by_label(subtopic).check()

@when('the user fills in "{value}" as the Next release')
def user_fills_in_next_release(context, value):
    context.page.get_by_label("Next release").fill(value)

@when('the user fills in "{value}" as the Keywords')
def user_fills_in_keywords(context, value):
    context.page.get_by_label("Keywords").fill(value)

@when('the user fills in "{value}" as the contact Name')
def user_fills_in_contact_name(context, value):
    context.page.get_by_label("Name").fill(value)

@when('the user fills in "{value}" as the contact Email')
def user_fills_in_contact_email(context, value):
    context.page.get_by_label("Email").fill(value)

@when("the user clicks Add contact")
def user_clicks_add_contact(context):
    context.page.get_by_role("button", name="Add contact").click()

@when("the user clicks Create dataset series")
def user_clicks_create_dataset_series(context):
    context.page.get_by_role("button", name="Create dataset series").click()
    context.page.wait_for_url("**/series/**")

@then("the Dataset Catalogue Manager heading is visible")
def dcm_heading_is_visible(context):
    expect(context.page.get_by_text("Dataset Catalogue Manager")).to_be_visible()

@then("the navigation links are visible")
def navigation_links_are_visible(context):
    expect(context.page.get_by_role("link", name="Dataset catalogue")).to_be_visible()

@then("the series list page should be visible")
def series_list_page_should_be_visible(context):
    expect(context.page.get_by_role("button", name="Create new series")).to_be_visible()

@then('the "{dataset_title}" dataset should be listed')
def dataset_should_be_listed(context, dataset_title):
    expect(context.page.get_by_role("link", name=dataset_title)).to_be_visible()

@then("the generated dataset should be listed")
def generated_dataset_should_be_listed(context):
    expect(context.page.get_by_text("Dataset series saved.")).to_be_visible()
    expect(context.page.get_by_role("heading", name=context.series_title)).to_be_visible()

@when('the user searches for "{search_term}" in the search box')
def user_searches_in_search_box(context, search_term):
    context.page.get_by_label("Search by ID").fill(search_term)
    context.page.get_by_test_id("series-list-search-by-id-button").click()
    context.page.wait_for_url(f"**/series?id={search_term}")

@then('a dataset with the Series ID "{series_id}" should be visible')
def dataset_with_series_id_should_be_visible(context, series_id):
    expect(context.page.get_by_text(f"Series ID: {series_id}")).to_be_visible()
    expect(context.page.get_by_text("Showing 1 to 1 of 1 series")).to_be_visible()

@then('no results should be found for "{search_term}"')
def no_results_found(context, search_term):
    expect(context.page.get_by_text(f"No results found for {search_term}")).to_be_visible()
