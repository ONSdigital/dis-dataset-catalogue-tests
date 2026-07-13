from playwright.sync_api import sync_playwright


def before_all(context):
    """Runs once before all tests. Sets up playwright browser and authenticates"""
    context.playwright = sync_playwright().start()
    context.browser = context.playwright.chromium.launch(headless=True)
    browser_context = context.browser.new_context()

    # Log in and extract access token
    page = browser_context.new_page()
    page.goto("http://localhost:29500/florence/login")
    page.get_by_label("John Smith (admin@ons.gov.uk)").click()
    page.get_by_role("button", name="Login").click()
    page.wait_for_load_state("networkidle")
    cookies = browser_context.cookies()
    token = next(c["value"] for c in cookies if c["name"] == "access_token")
    context.access_token = token.strip('"')
    browser_context.close()


def before_scenario(context, scenario):
    """Runs before each scenario. Creates a new browser context and page"""
    context.browser_context = context.browser.new_context()
    context.browser_context.add_cookies([{
        "name": "access_token",
        "value": f'"{context.access_token}"',
        "domain": "localhost",
        "path": "/"
    }])
    context.page = context.browser_context.new_page()


def after_scenario(context, scenario):
    """Runs after each scenario. Closes the browser context"""
    context.page.close()
    context.browser_context.close()


def after_all(context):
    """Runs once after all tests. Cleans up playwright"""
    context.browser.close()
    context.playwright.stop()