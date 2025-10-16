from playwright.sync_api import Page

class BasePage:
    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url

    def goto(self, path: str = ""):
        self.page.goto(self.base_url.rstrip("/") + "/" + path.lstrip("/"))

    def wait_network_idle(self, timeout: int = 30000):
        self.page.wait_for_load_state("networkidle", timeout=timeout)
