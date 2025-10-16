import os
from pages.upload_page import UploadPage
from pages.results_page import ResultsPage
from math import isclose

SAMPLE = "fixtures/sample_files/sample_2.spc"

def test_results_numeric_accuracy(page):
    base = os.getenv("BASE_URL", "http://localhost:8080")
    up = UploadPage(page, base)
    up.open()
    up.upload_sample(SAMPLE)
    up.start_analysis()
    rp = ResultsPage(page)
    assert isclose(rp.get_peak_value(), 125.3, rel_tol=1e-3)
