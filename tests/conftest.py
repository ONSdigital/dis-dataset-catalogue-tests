import pytest
from playwright.sync_api import sync_playwright

AUTH_URL = "http://localhost:29500/florence/login"

@pytest.fixture(scope="session")
def access_token():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        page.goto(AUTH_URL)
        page.get_by_label("John Smith (admin@ons.gov.uk)").click()
        page.get_by_role("button", name="Login").click()
        page.wait_for_load_state("networkidle")
        cookies = context.cookies()
        token = next(c["value"] for c in cookies if c["name"] == "access_token")
        token = token.strip('"')
        browser.close()
        return token

@pytest.fixture
def dataset_api_url():
    return "http://localhost:22000"

@pytest.fixture
def dcm_page(access_token):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        context.add_cookies([{
            "name": "access_token",
            "value": f'"{access_token}"',
            "domain": "localhost",
            "path": "/"
        }])
        page = context.new_page()
        yield page
        browser.close()