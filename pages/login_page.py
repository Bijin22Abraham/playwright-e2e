from playwright.sync_api import Page
from pages.base_page import BasePage

class LoginPage(BasePage):
    def open(self):
        self.goto("/login")

    def login(self, username: str, password: str):
        self.page.get_by_label("Username").fill(username)
        self.page.get_by_label("Password").fill(password)
        self.page.get_by_role("button", name="Sign in").click()
        self.wait_network_idle()
