from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
from Login import login

def manual_case_entry(driver):
    # List of case numbers
    case_numbers = ["081-CR-0022", "080-CR-0141"]

    for case in case_numbers:
        try:
            # Click on Add New Button
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='+ Add New']"))
            ).click()
            time.sleep(2)

            # Select "Special Court" from dropdown
            drop_down = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "select"))
            )
            select = Select(drop_down)
            select.select_by_visible_text("Special Court")

            # Enter the case number
            case_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@placeholder='मुद्दा नं:']"))
            )

            case_input.clear()
            case_input.send_keys(case)  # Enter the case number
            time.sleep(2)
            case_input.send_keys(Keys.ENTER)

            # Wait for the popup message (max 4 sec)
            popup = WebDriverWait(driver, 4).until(
                EC.presence_of_element_located((By.XPATH, "//section[@aria-label='Notifications Alt+T']"))
            )
            time.sleep(2)

            # Extract and print the message
            message_text = popup.text.strip()
            print(f"{case} : {message_text}")

            time.sleep(5)  # Pause before next entry
        
        except Exception as e:
            print(f"Error processing case {case}: {e}")

# Login and start case entry
driver = login()

if driver:
    manual_case_entry(driver)
