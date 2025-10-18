from pathlib import Path
from playwright.sync_api import Page, TimeoutError as PWTimeoutError
from pages.base_page import BasePage

class UploadPage(BasePage):
    def open(self):
        self.goto("/analyze")

    def upload_sample(self, file_path: str, timeout: int = 10000):
        """
        Attach a file to the input[type=file]. Ensures the input is visible and file exists.
        """
        p = Path(file_path)
        if not p.exists():
            raise FileNotFoundError(f"Sample file not found: {file_path}")

        file_input = self.page.locator("input[type=file]")
  
        try:
            file_input.wait_for(state="visible", timeout=timeout)
        except PWTimeoutError:
            raise RuntimeError("The file input did not become visible in time.")

       
        file_input.set_input_files(str(p))

    def start_analysis(self):
      
        self.page.get_by_role("button", name="Start Analysis").click(timeout=5000)
        self.page.wait_for_selector(".analysis-status:has-text('Completed')", timeout=120000)
