# Adding Scraped Case to System
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from Login import login
from Scraper import scrape_cases

def handle_popup(driver, case):
    """Handles popup messages and closes them."""

    # Wait for popup to appear (max 4 sec)
    popup = WebDriverWait(driver, 4).until(
        EC.presence_of_element_located((By.XPATH, "//section[@aria-label='Notifications Alt+T']"))
    )
    message_text = popup.text.strip()
    print(f"{case} - {message_text}") 

    try:
        # Click close button
        close_button = WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@class='btn btn-sm btn-circle btn-ghost absolute right-2 top-2']//*[name()='svg']"))
        )
        close_button.click()
        
    except Exception as e:
        print(f"Case added Successfully")

def add_scraped_case(driver):
    """Adds scraped cases using the same logged-in session."""
    
    case_numbers = scrape_cases(return_only_cases=True)

    for case in case_numbers:
        try:
            # Click "Add New" button
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='+ Add New']"))
            ).click()
            time.sleep(2)

            # Select "Debt Recovery Tribunal" from dropdown
            drop_down = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "select"))
            )
            select = Select(drop_down)
            select.select_by_visible_text("Debt Recovery Tribunal")

            # Enter the case number
            case_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@placeholder='मुद्दा नं:']"))
            )
            case_input.clear()
            case_input.send_keys(case)

            # Click Import Case button
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Import Case']"))
            ).click()
            time.sleep(3)  

            handle_popup(driver, case)  # Handle popup messages
        except Exception as e:
            print(f"Error processing case {case}: {e}")

# Run the script
driver = login()

if driver:
    add_scraped_case(driver)
    driver.quit()  
