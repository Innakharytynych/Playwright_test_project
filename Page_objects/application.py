import logging
from playwright.sync_api import Playwright
from playwright.sync_api import Request, Route, ConsoleMessage, Dialog
from .test_cases import TestCases


class App:
    def __init__(self, playwright: Playwright, base_url: str, headless=False, device=None, **kwargs):
        device_config = playwright.devices.get(device)
        if device_config is not None:
            device_config.update(kwargs)
        else:
            device_config = kwargs
        self.browser = playwright.chromium.launch(headless=headless)
        self.context = self.browser.new_context(**device_config)
        self.page = self.context.new_page()
        self.base_url = base_url
        self.test_cases = TestCases(self.page)

    def goto(self, endpoint: str, use_base_url=True):
        if use_base_url:
            self.page.goto(self.base_url + endpoint)
        else:
            self.page.goto(endpoint)

    def navigate_to(self, menu: str):
        self.page.click(f"css=header >> text =\"{menu}\"")

    def login(self, login: str, password: str):
        self.page.get_by_label("Username:").fill(login)
        self.page.get_by_label("Password:").fill(password)
        self.page.get_by_role("button", name="Login").click()

    def create_test(self, test_name: str, test_description: str):
        self.page.get_by_role("link", name="Create new test").click()
        self.page.locator("#id_name").fill(test_name)
        self.page.get_by_label("Test description").fill(test_description)
        self.page.get_by_role("button", name="Create").click()

    def intercept_request(self, url: str, payload: str):
        def handler(route: Route, request: Request):
            route.fulfill(status=200, body=payload)

        self.page.route(url, handler)

    def stop_intercept(self, url: str):
        self.page.unroute(url)

    def refresh_dashboard(self):
        self.page.click('input')

    def get_total_tests_stats(self):
        return self.page.text_content('.total >> span')

    def close(self):
        self.page.close()
        self.context.close()
        self.browser.close()
