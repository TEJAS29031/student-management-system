import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

@pytest.fixture
def driver():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')

    driver = webdriver.Chrome(options=chrome_options)
    driver.set_window_size(1920, 1080)
    yield driver
    driver.quit()

def test_app_loads(driver):
    driver.get("http://localhost:8501")

    wait = WebDriverWait(driver, 20)

    # Wait until app loads properly
    wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//*[contains(text(), 'Student Management System')]")
        )
    )

    assert "Student Management System" in driver.page_source

def test_navigation_exists(driver):
    driver.get("http://localhost:8501")
    time.sleep(5)

    assert "Dashboard" in driver.page_source
    assert "Add Student" in driver.page_source
    assert "View Students" in driver.page_source

def test_dashboard_metrics(driver):
    driver.get("http://localhost:8501")
    time.sleep(5)

    assert "Dashboard" in driver.page_source or "Total Students" in driver.page_source