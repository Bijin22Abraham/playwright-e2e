import os
from applitools.playwright import Eyes, Target

def test_chart_visual(page):
    eyes = Eyes()
    eyes.api_key = os.getenv("APPLITOOLS_API_KEY", "")
    BASE = os.getenv("BASE_URL", "http://localhost:8080")
    page.goto(BASE + "/results")
    try:
        eyes.open(page, app_name="MIRA", test_name="Chart Visual")
        eyes.check("Spectra Chart", Target.window().fully())
        eyes.close()
    finally:
        eyes.abort_if_not_closed()
