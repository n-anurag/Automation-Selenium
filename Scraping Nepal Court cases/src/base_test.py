from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import config
import time

class BaseTest:
    def setup_method(self):
        """Setup WebDriver before each test."""
        self.driver = webdriver.Chrome()
        self.driver.get(config.BASE_URL)
        self.driver.maximize_window()
        self.login(config.USERNAME, config.PASSWORD)

    def login(self, username, password):
        """Reusable login function."""
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Email Address']"))
        ).send_keys(username)

        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Password (8+ characters)']"))
        ).send_keys(password)

        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='LOGIN']"))
        ).click()
        time.sleep(5)
        try:
            success_message = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//h1[normalize-space()='Dashboard']"))
            )
            assert success_message.text == "Dashboard"
            print("Login Successful")
        except:
            print("Login Failed")
            self.driver.quit()

    def teardown_method(self):
        """Quit WebDriver after each test."""
        self.driver.quit()
