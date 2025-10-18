import os
import sys
import json
import time
from pathlib import Path

import pytest
from playwright.sync_api import sync_playwright, Playwright


sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

ARTIFACTS_DIR = Path("artifacts")
TEST_MODE = os.getenv("TEST_MODE", "stub").lower()
BASE_URL = os.getenv("BASE_URL", "http://localhost:8080")

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)


@pytest.fixture(scope="session")
def pw():
    with sync_playwright() as p:
        yield p

@pytest.fixture(scope="session")
def browser(pw: Playwright):
   
    browser = pw.chromium.launch(headless=True)
    yield browser
    browser.close()

@pytest.fixture(scope="function")
def context(request, browser):
    ctx = browser.new_context()
    ctx.tracing.start(screenshots=True, snapshots=True, sources=True)
    yield ctx


    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    trace_path = ARTIFACTS_DIR / f"trace-{request.node.name}-{int(time.time())}.zip"
    rep_call = getattr(request.node, "rep_call", None)
    try:
        if rep_call and getattr(rep_call, "outcome", "") == "failed":
            ctx.tracing.stop(path=str(trace_path))
            print(f"[TRACE] Saved trace to: {trace_path}")
        else:
            ctx.tracing.stop()
    except Exception as e:
        print("[TRACE] failed to save trace:", e)
    ctx.close()

@pytest.fixture(scope="function")
def page(context):
    page = context.new_page()
    yield page
    page.close()


_LOGIN_HTML = "<html><body><h1>Dashboard</h1></body></html>"
_ANALYZE_HTML = """
<html>
  <body>
    <h1>Analyze</h1>
    <!-- make the file input visible & labelled so Playwright can interact reliably -->
    <label for="file">Sample file</label>
    <input type='file' id='file' name='file' style='display:block; width:300px; height:28px; opacity:1;' />
    <button id='start'>Start Analysis</button>
    <div class='analysis-status'>Completed</div>
    <div class='result-peak-value'>42.0</div>
  </body>
</html>
"""
_RESULTS_HTML = "<html><body><h1>Results</h1><div class='result-peak-value'>42.0</div><button id='export'>Export CSV</button></body></html>"

@pytest.fixture(scope="function")
def stub_routes(page):
    """
    Install default in-test stubs when TEST_MODE=stub (default).
    Add `stub_routes` as a fixture parameter in tests that should use stubs.
    """
    if TEST_MODE != "stub":
        yield
        return


    page.route("**/api/analysis", lambda route, req: route.fulfill(
        status=200,
        content_type="application/json",
        body=json.dumps({"runId":"abc","status":"completed","results":{"peak":42.0}})
    ))

   
    page.route("**/analyze", lambda route, req: route.fulfill(
        status=200, content_type="text/html", body=_ANALYZE_HTML
    ))
    page.route("**/login", lambda route, req: route.fulfill(
        status=200, content_type="text/html", body=_LOGIN_HTML
    ))
    page.route("**/results", lambda route, req: route.fulfill(
        status=200, content_type="text/html", body=_RESULTS_HTML
    ))

    yield
 
