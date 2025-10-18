# tests/test_upload_and_analysis.py
import os
from pages.upload_page import UploadPage
from pages.results_page import ResultsPage

SAMPLE = "fixtures/sample_files/sample_1.spc"

def test_upload_and_analysis_with_stub(page, stub_routes):
    base = os.getenv("BASE_URL", "http://localhost:8080")
    up = UploadPage(page, base)
    up.open()
    up.upload_sample(SAMPLE)
    up.start_analysis()
    rp = ResultsPage(page)
    assert rp.get_peak_value() == 42.0
