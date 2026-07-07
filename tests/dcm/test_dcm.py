from playwright.sync_api import expect

DCM_URL = "http://localhost:29400/data-admin"

def test_dcm_homepage(dcm_page, access_token):
    dcm_page.goto(DCM_URL)
    expect(dcm_page.get_by_text("Dataset Catalogue Manager")).to_be_visible()
    expect(dcm_page.get_by_role("heading", name="Home")).to_be_visible()
    expect(dcm_page.get_by_role("link", name="Dataset catalogue")).to_be_visible()
