import random
import string

import requests
from behave import given, when, then

from features.utils import (
    _post_dataset,
    _post_dataset_with_multiple_editions,
    _post_dataset_with_multiple_versions,
    _post_version,
    _post_file_metadata,
)

DATASET_API_URL = "http://localhost:22000"


@given("the dataset API is available")
def dataset_api_is_available(context):
    context.dataset_api_url = DATASET_API_URL
    context.headers = {"Authorization": context.access_token}


@when("I request a list of datasets")
def request_list_of_datasets(context):
    context.response = requests.get(
        f"{context.dataset_api_url}/datasets", headers=context.headers
    )


@when('I request the dataset with ID "{dataset_id}"')
def request_dataset_by_id(context, dataset_id):
    _post_dataset(context, dataset_id)
    context.response = requests.get(
        f"{context.dataset_api_url}/datasets/{context.dataset_id}",
        headers=context.headers,
    )


@when('I request the editions for dataset with ID "{dataset_id}"')
def request_dataset_editions(context, dataset_id):
    _post_dataset_with_multiple_editions(context, dataset_id, 2)
    context.response = requests.get(
        f"{context.dataset_api_url}/datasets/{context.dataset_id}/editions",
        headers=context.headers,
    )


@when('I request the edition with ID "{edition_id}" for dataset with ID "{dataset_id}"')
def request_dataset_edition(context, dataset_id, edition_id):
    _post_dataset(context, dataset_id)
    _post_version(context, edition_id, 1)

    context.response = requests.get(
        f"{context.dataset_api_url}/datasets/{context.dataset_id}/editions/{context.edition_id}",
        headers=context.headers,
    )


@when(
    'I request the versions for edition ID "{edition_id}" and dataset ID "{dataset_id}"'
)
def request_dataset_versions(context, dataset_id, edition_id):
    _post_dataset_with_multiple_versions(context, dataset_id, edition_id, 2)
    context.response = requests.get(
        f"{context.dataset_api_url}/datasets/{context.dataset_id}/editions/{context.edition_id}/versions",
        headers=context.headers,
    )


@when(
    'I request version "{version}" for edition ID "{edition_id}" and dataset ID "{dataset_id}"'
)
def request_dataset_version(context, dataset_id, edition_id, version):
    _post_dataset(context, dataset_id)
    _post_version(context, edition_id, version)
    context.response = requests.get(
        f"{context.dataset_api_url}/datasets/{context.dataset_id}/editions/{context.edition_id}/versions/{version}",
        headers=context.headers,
    )


@when(
    'I request the metadata for dataset ID "{dataset_id}", edition ID "{edition_id}", version "{version}"'
)
def request_version_metadata(context, dataset_id, edition_id, version):
    _post_dataset(context, dataset_id)
    _post_version(context, edition_id, version)
    context.response = requests.get(
        f"{context.dataset_api_url}/datasets/{context.dataset_id}/editions/{context.edition_id}/versions/{version}/metadata",
        headers=context.headers,
    )


@when('I add a new dataset with ID "{dataset_id}"')
def add_dataset(context, dataset_id):
    context.response = _post_dataset(context, dataset_id)


@when('I update the dataset "{dataset_id}" with title "{new_title}"')
def update_dataset(context, dataset_id, new_title):
    _post_dataset(context, dataset_id)
    put_body = {
        "id": context.dataset_id,
        "title": f"{new_title} for {context.dataset_id}",
        "description": "New dataset description",
        "next_release": "2026-12-31T00:00:00.000Z",
        "license": "Open Government Licence v3.0",
        "keywords": ["Keyword 1"],
        "contacts": [{"email": "jdoe@ons.gov.uk", "name": "Jane Doe"}],
        "topics": ["topic-0"],
    }
    context.response = requests.put(
        f"{context.dataset_api_url}/datasets/{context.dataset_id}",
        json=put_body,
        headers=context.headers,
    )


@when('I delete the dataset "{dataset_id}"')
def delete_dataset(context, dataset_id):
    _post_dataset(context, dataset_id)
    context.response = requests.delete(
        f"{context.dataset_api_url}/datasets/{context.dataset_id}",
        headers=context.headers,
    )


@when('I add a new version for dataset ID "{dataset_id}" and edition ID "{edition_id}"')
def add_version(context, dataset_id, edition_id):
    _post_dataset(context, dataset_id)
    context.response = _post_version(context, edition_id, 1)


@when(
    'I add a new version for dataset ID "{dataset_id}", edition ID "{edition_id}" and version "{version}"'
)
def add_version_with_id(context, dataset_id, edition_id, version):
    _post_dataset(context, dataset_id)
    random_edition_id = f"{edition_id}-{"".join(random.choice(string.ascii_lowercase) for i in range(4))}"
    random_filename = (
        f"{"".join(random.choice(string.ascii_lowercase) for i in range(8))}.csv"
    )
    version_body = {
        "distributions": [
            {
                "title": "CSV distribution",
                "download_url": f"{context.dataset_id}/{random_edition_id}/1/{random_filename}",
                "format": "csv",
            }
        ],
        "edition_title": f"Edition {random_edition_id}",
        "release_date": "2026-12-31T00:00:00.000Z",
        "type": "static",
    }
    context.response = requests.post(
        f"{context.dataset_api_url}/datasets/{context.dataset_id}/editions/{random_edition_id}/versions/{version}",
        json=version_body,
        headers=context.headers,
    )


@when(
    'I update version "{version}" for dataset ID "{dataset_id}", edition ID "{edition_id}"'
)
def update_version(context, dataset_id, edition_id, version):
    _post_dataset(context, dataset_id)
    _post_version(context, edition_id, version)
    update_version_body = {
        "edition_title": "New edition title",
        "type": "static",
    }
    context.response = requests.put(
        f"{context.dataset_api_url}/datasets/{context.dataset_id}/editions/{context.edition_id}/versions/{version}",
        json=update_version_body,
        headers=context.headers,
    )


@when(
    'I update the state to "{state}" for version "{version}" for dataset ID "{dataset_id}", edition ID "{edition_id}"'
)
def update_version_state(context, dataset_id, edition_id, version, state):
    _post_dataset(context, dataset_id)
    _post_version(context, edition_id, version)
    _post_file_metadata(context, version)
    put_state_body = {"type": "static", "state": state}
    context.response = requests.put(
        f"{context.dataset_api_url}/datasets/{context.dataset_id}/editions/{context.edition_id}/versions/{version}",
        json=put_state_body,
        headers=context.headers,
    )


@when(
    'I delete version "{version}" for dataset ID "{dataset_id}", edition ID "{edition_id}"'
)
def delete_version(context, dataset_id, edition_id, version):
    _post_dataset(context, dataset_id)
    _post_version(context, edition_id, version)
    _post_file_metadata(context, version)
    context.response = requests.delete(
        f"{context.dataset_api_url}/datasets/{context.dataset_id}/editions/{context.edition_id}/versions/{version}",
        headers=context.headers,
    )


@then('the response status code should be "{status_code}"')
def response_status_code_should_be(context, status_code):
    assert context.response.status_code == int(status_code)


@then("the response should contain a list of items")
def response_should_contain_list_of_items(context):
    data = context.response.json()
    assert "items" in data
    assert "total_count" in data


@then("the response should contain the requested dataset")
def response_should_contain_dataset(context):
    data = context.response.json()
    assert data["id"] == context.dataset_id


@then("the response should contain the requested edition")
def response_should_contain_edition(context):
    data = context.response.json()
    assert data["next"]["edition"] == context.edition_id


@then('the response should contain the version with ID "{version}"')
def response_should_contain_version(context, version):
    data = context.response.json()
    assert data["version"] == int(version)


@then('the response should contain the version with state "{state}"')
def response_should_contain_version_with_state(context, state):
    data = context.response.json()
    assert data["state"] == state


@then('the response should contain the metadata for version "{version}"')
def response_should_contain_metadata(context, version):
    data = context.response.json()
    assert data["version"] == int(version)


@then('the response should include the updated dataset title "{new_title}"')
def response_should_contain_new_dataset_title(context, new_title):
    data = context.response.json()
    assert new_title in data["title"]


@then('the response should include the updated edition title "{new_title}"')
def response_should_contain_new_edition_title(context, new_title):
    data = context.response.json()
    assert new_title in data["edition_title"]
