import csv
from playwright.sync_api import sync_playwright


def make_cookie(name, value):
    return {
        "name": name,
        "value": value,
        "domain": "localhost",
        "path": "/",
        "httpOnly": True,
        "secure": False,
        "sameSite": "Lax"
    }


def before_all(context):
    """Runs once before all tests. Sets up playwright browser and authenticates"""
    context.test_csv_path = "/tmp/smoke-test-dataset.csv"
    with open(context.test_csv_path, "w") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "value"])
        writer.writerow(["1", "test"])

    context.playwright = sync_playwright().start()
    context.browser = context.playwright.chromium.launch(headless=False, slow_mo=500)
    browser_context = context.browser.new_context()

    # Log in and extract access token
    page = browser_context.new_page()
    page.goto("http://localhost:29500/florence/login")
    page.get_by_label("John Smith (admin@ons.gov.uk)").click()
    page.get_by_role("button", name="Login").click()
    page.wait_for_load_state("networkidle")
    cookies = browser_context.cookies()
    access_cookie = next(c for c in cookies if c["name"] == "access_token")
    id_token = next(c["value"] for c in cookies if c["name"] == "id_token")
    context.access_token = access_cookie["value"].strip('"')
    context.id_token = id_token.strip('"')
    browser_context.close()


def before_scenario(context, scenario):
    """Runs before each scenario. Creates a new browser context and page"""
    context.browser_context = context.browser.new_context()
    context.browser_context.add_cookies([
        make_cookie("access_token", f'"{context.access_token}"'),
        make_cookie("id_token", context.id_token),
    ])
    context.page = context.browser_context.new_page()


def after_scenario(context, scenario):
    """Runs after each scenario. Closes the browser context and cleans up"""
    import requests
    headers = {"Authorization": context.access_token}

    # cleans up generated series after series/edition creation tests
    if hasattr(context, 'series_id'):
        requests.delete(
            f"http://localhost:22000/datasets/{context.series_id}",
            headers=headers
        )

    # cleans up unpublshed version after version creation test
    if scenario.name == "User creates a new version for a dataset edition":
        response = requests.get(
            "http://localhost:22000/datasets/static-test-dataset/editions/time-series/versions",
            headers=headers
        )
        data = response.json()
        for version in data["items"]:
            if version["state"] != "published":
                version_number = version["version"]
                requests.delete(
                    f"http://localhost:22000/datasets/static-test-dataset/editions/time-series/versions/{version_number}",
                    headers=headers
                )
                break

    context.page.close()
    context.browser_context.close()

def after_all(context):
    """Runs once after all tests. Cleans up playwright"""
    context.browser.close()
    context.playwright.stop()