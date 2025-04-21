import pytest
import sys
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Ensure correct path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from pages.login import login # ✅ Import login function from pages.login

@pytest.fixture
def driver():
    """Fixture to initialize and quit the browser after test execution."""
    driver = webdriver.Chrome()
    driver.get("https://demo.opencart.com/index.php?route=account/login")  # OpenCart login page
    driver.maximize_window()
    yield driver  # Return driver instance for tests
    driver.quit()  # Close browser after tests

# ✅ Test Case 1: Valid Login
def test_valid_login(driver):
    username = "nanurag965@gmail.com"
    password = "anurag123"

    login(driver, username, password)

    # Check if login was successful
    success_message = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, "//h2[normalize-space()='My Account']"))
    )
    assert success_message.text == "My Account", "❌ Login Failed! Expected 'My Account' page."

# ✅ Test Case 2: Invalid Login
def test_invalid_login(driver):
    username = "wrongemail@example.com"
    password = "wrongpassword"

    login(driver, username, password)

    try:
        # Check if alert message appears
        error_message = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'alert-danger')]"))
        )
        assert "Warning" in error_message.text, "❌ Expected warning message not displayed."
    except:
        pytest.fail("❌ Login error message not found!")
