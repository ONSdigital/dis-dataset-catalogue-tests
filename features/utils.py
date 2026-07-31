import random
import string

import requests
from uuid import uuid4
from pymongo import MongoClient

FILES_API_URL = "http://localhost:26900"
MONGO_URL = "mongodb://localhost:27017"


def _get_mongo_dataset_record_by_id(dataset_id,):
    mongo_client = MongoClient(MONGO_URL)
    try:
        return mongo_client["datasets"]["datasets"].find_one(
            {"_id": dataset_id}
        )
    finally:
        mongo_client.close()


def _post_dataset(context, dataset_id):
    context.dataset_id = f"{dataset_id}-{"".join(random.choice(string.ascii_lowercase) for i in range(4))}"
    dataset_body = {
        "id": context.dataset_id,
        "title": f"{context.dataset_id}",
        "description": "Dataset description",
        "next_release": "2026-12-31T00:00:00.000Z",
        "license": "Open Government Licence v3.0",
        "keywords": ["Keyword 1"],
        "contacts": [{"email": "jdoe@ons.gov.uk", "name": "Jane Doe"}],
        "topics": ["topic-0"],
        "type": "static",
    }
    post_dataset_response = requests.post(
        f"{context.dataset_api_url}/datasets",
        json=dataset_body,
        headers=context.headers,
    )
    return post_dataset_response


def _post_version(context, edition_id, version):
    context.edition_id = f"{edition_id}-{"".join(random.choice(string.ascii_lowercase) for i in range(4))}"
    context.filename = (
        f"{"".join(random.choice(string.ascii_lowercase) for i in range(8))}.csv"
    )
    context.path = f"{uuid4()}/{context.filename}"
    version_body = {
        "distributions": [
            {
                "title": "CSV distribution",
                "download_url": context.path,
                "format": "csv",
            }
        ],
        "edition_title": f"{context.edition_id}",
        "release_date": "2026-12-31T00:00:00.000Z",
        "type": "static",
    }
    post_version_response = requests.post(
        f"{context.dataset_api_url}/datasets/{context.dataset_id}/editions/{context.edition_id}/versions",
        json=version_body,
        headers=context.headers,
    )
    return post_version_response


def _post_versions(context, edition_id, num_versions):
    context.edition_id = f"{edition_id}-{"".join(random.choice(string.ascii_lowercase) for i in range(4))}"
    context.filename = (
        f"{"".join(random.choice(string.ascii_lowercase) for i in range(8))}.csv"
    )
    context.path = f"{uuid4()}/{context.filename}"
    for i in range(num_versions):
        version_body = {
            "distributions": [
                {
                    "title": "CSV distribution",
                    "download_url": context.path,
                    "format": "csv",
                }
            ],
            "edition_title": f"{context.edition_id}",
            "release_date": "2026-12-31T00:00:00.000Z",
            "type": "static",
        }
        requests.post(
            f"{context.dataset_api_url}/datasets/{context.dataset_id}/editions/{context.edition_id}/versions",
            json=version_body,
            headers=context.headers,
        )
        _post_file_metadata(context, i)


def _post_file_metadata(context, version):
    file_metadata_body = {
        "path": context.path,
        "is_publishable": True,
        "title": "Data CSV",
        "size_in_bytes": 458,
        "type": "text/csv",
        "licence": "Open Government Licence v3.0",
        "licence_url": "http://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/",
        "content_item": {
            "dataset_id": context.dataset_id,
            "edition": context.edition_id,
            "version": f"{version}",
        },
        "etag": "some-etag",
    }
    requests.post(
        f"{FILES_API_URL}/files", json=file_metadata_body, headers=context.headers
    )
    requests.patch(
        f"{FILES_API_URL}/files/{context.path}",
        json={"state": "UPLOADED", "etag": "etag"},
        headers=context.headers,
    )


def _post_dataset_with_multiple_editions(context, dataset_id, num_editions):
    _post_dataset(context, dataset_id)
    for i in range(num_editions):
        _post_version(context, f"edition-{i}", 1)


def _post_dataset_with_multiple_versions(context, dataset_id, edition_id, num_versions):
    _post_dataset(context, dataset_id)
    _post_versions(context, edition_id, num_versions)
