from playwright.sync_api import Page

class ResultsPage:
    def __init__(self, page: Page):
        self.page = page

    def get_peak_value(self):
        txt = self.page.locator(".result-peak-value").inner_text()
        return float(txt.replace(",", "").strip())

    def export_csv(self):
        with self.page.expect_download() as download_info:
            self.page.get_by_role("button", name="Export CSV").click()
        download = download_info.value
        path = download.path()
        return path
