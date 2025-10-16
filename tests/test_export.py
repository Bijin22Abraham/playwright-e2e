import os
from pages.upload_page import UploadPage
from pages.results_page import ResultsPage

SAMPLE = "fixtures/sample_files/sample_3.spc"

def test_export_csv(page, tmp_path):
    base = os.getenv("BASE_URL", "http://localhost:8080")
    up = UploadPage(page, base)
    up.open()
    up.upload_sample(SAMPLE)
    up.start_analysis()
    rp = ResultsPage(page)
    
    csv_path = rp.export_csv()
    assert csv_path is not None

