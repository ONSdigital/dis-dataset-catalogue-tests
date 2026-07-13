import requests
from behave import given, when, then

DATASET_API_URL = "http://localhost:22000"

@given("the dataset API is available")
def dataset_api_is_available(context):
    context.dataset_api_url = DATASET_API_URL
    context.headers = {"Authorization": context.access_token}

@when('I request a list of datasets')
def request_list_of_datasets(context):
    context.response = requests.get(f"{context.dataset_api_url}/datasets", headers=context.headers)

@when('I request the dataset with ID "{dataset_id}"')
def request_dataset_by_id(context, dataset_id):
    context.dataset_id = dataset_id
    context.response = requests.get(f"{context.dataset_api_url}/datasets/{dataset_id}", headers=context.headers)

@when('I request the editions for dataset with ID "{dataset_id}"')
def request_dataset_editions(context, dataset_id):
    context.response = requests.get(f"{context.dataset_api_url}/datasets/{dataset_id}/editions", headers=context.headers)

@then("the response status code should be 200")
def response_status_code_should_be_200(context):
    assert context.response.status_code == 200

@then("the response should contain a list of items")
def response_should_contain_list_of_items(context):
    data = context.response.json()
    assert "items" in data
    assert "total_count" in data

@then('the response should contain the dataset with ID "{dataset_id}"')
def response_should_contain_dataset(context, dataset_id):
    data = context.response.json()
    assert data["id"] == dataset_id