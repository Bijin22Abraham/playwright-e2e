import os
from pages.login_page import LoginPage

def test_login(page):
    base = os.getenv("BASE_URL", "http://localhost:8080")
    lp = LoginPage(page, base)
    lp.open()

    assert page.get_by_text("Dashboard").is_visible()
