import sys
import os
import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from base_test import BaseTest

class TestLogin(BaseTest):
    
    def test_valid_login(self):
        """ Valid Login - Should Redirect to Dashboard"""
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//h1[normalize-space()='Dashboard']"))
        )
        assert "The Legalities" in self.driver.title  # Update based on actual title

    @pytest.mark.parametrize("username, password, expected_error", [
        ("wrongemail@gmail.com", "staging1234", "Invalid email or password"),   # ❌ Invalid Email
        ("stagingadmin@gmail.com", "wrongpassword", "Invalid email or password"), # ❌ Invalid Password
        
    ])
    def test_invalid_logins(self, username, password, expected_error):
        """❌ Invalid Login Attempts - Should Show Proper Error Messages"""
        self.login(username, password)  # Using the reusable login function

        # Wait for error message
        error_message_element = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='error-message']")) # Update with correct XPath
        )

        assert expected_error in error_message_element.text  # Validate error message

