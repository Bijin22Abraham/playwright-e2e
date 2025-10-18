import os
from pages.upload_page import UploadPage
from pages.results_page import ResultsPage

SAMPLE = "fixtures/sample_files/sample_3.spc"

def test_export_csv(page, stub_routes, tmp_path):
    base = os.getenv("BASE_URL", "http://localhost:8080")
    up = UploadPage(page, base)
    up.open()                     
    up.upload_sample(SAMPLE)
    up.start_analysis()           

    page.goto(base + "/results")
    rp = ResultsPage(page)

    assert page.get_by_role("button", name="Export CSV").is_visible() or page.locator("#export").is_visible()
