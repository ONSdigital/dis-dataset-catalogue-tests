import requests

DATASET_ID = "cpih01"

def test_get_datasets(dataset_api_url, access_token):
    headers = {"Authorization": access_token}
    response = requests.get(f"{dataset_api_url}/datasets", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total_count" in data

def test_get_dataset_by_id(dataset_api_url, access_token):
    headers = {"Authorization": access_token}
    response = requests.get(f"{dataset_api_url}/datasets/{DATASET_ID}", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == DATASET_ID

def test_get_dataset_editions(dataset_api_url, access_token):
    headers = {"Authorization": access_token}
    response = requests.get(f"{dataset_api_url}/datasets/{DATASET_ID}/editions", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total_count" in data