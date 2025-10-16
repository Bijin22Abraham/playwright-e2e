from playwright.sync_api import Page
from pages.base_page import BasePage

class UploadPage(BasePage):
    def open(self):
        self.goto("/analyze")

    def upload_sample(self, file_path: str):
        self.page.set_input_files("input[type=file]", file_path)

    def start_analysis(self):
        self.page.get_by_role("button", name="Start Analysis").click()
        self.page.wait_for_selector(".analysis-status:has-text('Completed')", timeout=120000)
