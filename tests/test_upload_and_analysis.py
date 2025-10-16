import os
from pages.upload_page import UploadPage
from pages.results_page import ResultsPage

SAMPLE = "fixtures/sample_files/sample_1.spc"

def test_upload_and_analysis_with_stub(page):
    def handle(route, request):
        body = {"runId": "abc123", "status": "completed", "results": {"peak": 42.0}}
        route.fulfill(status=200, body=json.dumps(body), headers={"Content-Type":"application/json"})

    page.route("**/api/analysis", lambda route, req: route.fulfill(status=200, body='{"runId":"abc","status":"completed","results":{"peak":42.0}}', headers={"Content-Type":"application/json"}))

    base = os.getenv("BASE_URL", "http://localhost:8080")
    up = UploadPage(page, base)
    up.open()
    up.upload_sample(SAMPLE)
    up.start_analysis()
    rp = ResultsPage(page)
    assert rp.get_peak_value() == 42.0
