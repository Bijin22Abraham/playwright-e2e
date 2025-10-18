import os
import pytest
from applitools.playwright import Eyes, Target

def test_chart_visual(page, stub_routes):
    key = os.getenv("APPLITOOLS_API_KEY")
    if not key:
        pytest.skip("APPLITOOLS_API_KEY not set - skipping visual test")

    eyes = Eyes()
    eyes.configure.set_api_key(key)
    base = os.getenv("BASE_URL", "http://localhost:8080")
    page.goto(base + "/results")
    eyes.open(page, app_name="MIRA", test_name="Chart Visual")
    eyes.check("Spectra Chart", Target.window().fully())
    eyes.close()
