from behave import given, then, when
from playwright.sync_api import expect

from features.utils import _post_dataset_with_multiple_editions, _post_version, _post_dataset, _post_file_metadata

OVERVIEW_BASE_URL = "http://localhost:20200"
DEFAULT_TOPIC_SLUG = "businessindustryandtrade"
OVERVIEW_PAGE_URL = f"{OVERVIEW_BASE_URL}/{DEFAULT_TOPIC_SLUG}/datasets"
DATASET_API_URL = "http://localhost:22000"


def _setup_context(context):
    context.dataset_api_url = DATASET_API_URL
    context.headers = {"Authorization": context.access_token}


def _collect_statuses(context, response):
    context.statuses = []
    r = response
    while r:
        context.statuses.append(str(r.status))
        r = r.request.redirected_from.response() if r.request.redirected_from else None


def _assert_json_response(context):
    content_type = context.response.headers.get("content-type", "")
    assert "application/json" in content_type.lower()


@given('the user navigates to the overview page for "{dataset_id}"')
def user_navigates_to_overview_page(context, dataset_id):
    _setup_context(context)
    _post_dataset_with_multiple_editions(context, dataset_id, 1)
    response = context.page.goto(f"{OVERVIEW_PAGE_URL}/{context.dataset_id}")
    _collect_statuses(context, response)


@given('the user navigates to the editions page for "{dataset_id}"')
def user_navigates_to_editions_page(context, dataset_id):
    _setup_context(context)
    _post_dataset_with_multiple_editions(context, dataset_id, 1)
    response = context.page.goto(f"{OVERVIEW_PAGE_URL}/{context.dataset_id}/editions")
    _collect_statuses(context, response)


@given('the user navigates to the overview page for series "{dataset_id}" with "{num_editions}" editions')
def user_navigates_to_overview_page_for_series_with_multiple_editions(context, dataset_id, num_editions):
    _setup_context(context)
    _post_dataset_with_multiple_editions(context, dataset_id, int(num_editions))
    response = context.page.goto(f"{OVERVIEW_PAGE_URL}/{context.dataset_id}/editions")
    _collect_statuses(context, response)


@given('the user navigates to the editions page for "{dataset_id}" with "{num_editions}" editions')
def user_navigates_to_editions_page_with_multiple_editions(context, dataset_id, num_editions):
    _setup_context(context)
    _post_dataset_with_multiple_editions(context, dataset_id, int(num_editions))
    response = context.page.goto(f"{OVERVIEW_PAGE_URL}/{context.dataset_id}/editions")
    _collect_statuses(context, response)


@given('the user navigates to the edition page for "{dataset_id}" with edition "{edition_id}"')
def user_navigates_to_edition_page(context, dataset_id, edition_id):
    _setup_context(context)
    _post_dataset(context, dataset_id)
    _post_version(context, edition_id, 1)
    response = context.page.goto(f"{OVERVIEW_PAGE_URL}/{context.dataset_id}/editions/{context.edition_id}")
    _collect_statuses(context, response)


@given('the user navigates to the versions page for "{dataset_id}" with edition "{edition_id}"')
def user_navigates_to_versions_page(context, dataset_id, edition_id):
    _setup_context(context)
    _post_dataset(context, dataset_id)
    _post_version(context, edition_id, 1)
    response = context.page.goto(f"{OVERVIEW_PAGE_URL}/{context.dataset_id}/editions/{context.edition_id}")
    _collect_statuses(context, response)


@given('the user navigates to the version page for "{dataset_id}" with edition "{edition_id}" and version "{version}"')
def user_navigates_to_version_page(context, dataset_id, edition_id, version):
    _setup_context(context)
    _post_dataset(context, dataset_id)
    _post_version(context, edition_id, 1)
    _post_file_metadata(context, 1)
    response = context.page.goto(
        f"{OVERVIEW_PAGE_URL}/{context.dataset_id}/editions/{context.edition_id}/versions/{version}"
    )
    _collect_statuses(context, response)


@given('the user navigates to the overview page for "{dataset_id}" using incorrect topic slug')
def user_navigates_to_overview_page_incorrect_topic_slug(context, dataset_id):
    _setup_context(context)
    _post_dataset(context, dataset_id)
    overview_page = f"{OVERVIEW_BASE_URL}/census"
    response = context.page.goto(f"{overview_page}/datasets/{context.dataset_id}")
    _collect_statuses(context, response)


@given('the user navigates to the data page for "{dataset_id}"')
def user_navigates_to_dataset_data_page(context, dataset_id):
    _setup_context(context)
    _post_dataset(context, dataset_id)
    context.response = context.page.goto(f"{OVERVIEW_PAGE_URL}/{context.dataset_id}/data")
    _collect_statuses(context, context.response)


@given('the user navigates to the data page for the edition of "{dataset_id}" and "{edition_id}"')
def user_navigates_to_edition_data_page(context, dataset_id, edition_id):
    _setup_context(context)
    _post_dataset(context, dataset_id)
    _post_version(context, edition_id, 1)
    context.response = context.page.goto(
        f"{OVERVIEW_PAGE_URL}/{context.dataset_id}/editions/{context.edition_id}/data"
    )
    _collect_statuses(context, context.response)


@given('the user navigates to the data page for the version of "{dataset_id}" and "{edition_id}"')
def user_navigates_to_version_data_page(context, dataset_id, edition_id):
    _setup_context(context)
    _post_dataset(context, dataset_id)
    _post_version(context, edition_id, 1)
    context.response = context.page.goto(
        f"{OVERVIEW_PAGE_URL}/{context.dataset_id}/editions/{context.edition_id}/versions/1/data"
    )
    _collect_statuses(context, context.response)


@then('there is a response code of "{status_code}"')
def response_code_is_visible(context, status_code):
    assert status_code in context.statuses


@then('the user is redirected to the version page at "{version_path}"')
def user_is_redirected_to_version_page_at(context, version_path):
    expect(context.page).to_have_url(f"{OVERVIEW_PAGE_URL}/{version_path}")


@then("the user is redirected to the latest version page")
def redirect_to_the_latest_version_page(context):
    expect(context.page).to_have_url(
        f"{OVERVIEW_PAGE_URL}/{context.dataset_id}/editions/{context.edition_id}/versions/1"
    )


@then("the user is redirected to the correct overview page")
def user_is_redirected_to_correct_overview_page(context):
    expect(context.page).to_have_url(f"{OVERVIEW_PAGE_URL}/{context.dataset_id}")


@then("the editions should be listed on the page")
def editions_should_be_listed_on_the_page(context):
    page_body = context.page.text_content("body")
    assert all(edition_id in page_body for edition_id in context.edition_ids)


@then("the version details should be displayed on the page")
def version_details_should_be_displayed_on_the_page(context):
    page_body = context.page.text_content("body")
    assert context.dataset_id in page_body
    assert context.edition_id in page_body
    assert "Version:" in page_body


@then("the response should contain the dataset details in JSON format")
def dataset_json_contains_dataset_details(context):
    _assert_json_response(context)
    data = context.response.json()
    assert data["description"]["title"] == context.dataset_id
    assert data["uri"] == f"/businessindustryandtrade/datasets/{context.dataset_id}"


@then("the response should contain the dataset edition details in JSON format")
def dataset_json_contains_edition_details(context):
    _assert_json_response(context)
    data = context.response.json()
    assert data["description"]["title"] == context.dataset_id
    assert data["description"]["edition"] == context.edition_id
    assert data["uri"] == f"/businessindustryandtrade/datasets/{context.dataset_id}/editions/{context.edition_id}"


@then("the response should contain the version details in JSON format")
def dataset_json_contains_version_details(context):
    _assert_json_response(context)
    data = context.response.json()
    assert data["description"]["title"] == context.dataset_id
    assert data["description"]["edition"] == context.edition_id
    assert data["uri"] == f"/businessindustryandtrade/datasets/{context.dataset_id}/editions/{context.edition_id}/versions/1"


@when("the user clicks the approve button")
def click_approve_button(context):
    context.page.get_by_role("button", name="Approve").click()


@then("the version page should show approved")
def page_should_show_approved(context):
    assert "Approved" in context.page.text_content("body")


@then("the user can click on one of the editions")
def click_on_edition(context):
    context.edition_id = context.edition_ids[1]
    context.page.get_by_role("link", name=context.edition_ids[1]).click()
