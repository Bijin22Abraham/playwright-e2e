import os
import time
import uuid
import pytest
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE_URL = os.getenv("BASE_URL", "http://localhost:8080")
ARTIFACTS_DIR = Path(os.getenv("ARTIFACTS_DIR", "artifacts"))

def pytest_runtest_makereport(item, call):
    if call.when == "call":
        setattr(item, "rep_call", call)

@pytest.fixture(scope="session")
def pw():
    with sync_playwright() as p:
        yield p

@pytest.fixture(scope="session")
def browser(pw):
    browser = pw.chromium.launch(headless=True)
    yield browser
    browser.close()

@pytest.fixture(scope="function")
def context(request, browser):
    ctx = browser.new_context()
    ctx.tracing.start(screenshots=True, snapshots=True, sources=True)
    yield ctx

    rep = getattr(request.node, "rep_call", None)
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    trace_path = ARTIFACTS_DIR / f"trace-{request.node.name}-{int(time.time())}.zip"
    try:
        if rep and rep.failed:
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
