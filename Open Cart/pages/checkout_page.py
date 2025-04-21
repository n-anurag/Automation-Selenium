from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from login import login  # Assuming login function is in login.py
from cart_page import add_to_cart

def checkout(driver):
    if driver is None:
        print("❌ No driver session found!")
        return



    # ✅ Wait until checkout button is present & clickable
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[@class='btn btn-primary']"))
    )

    driver.execute_script("window.scrollBy(0, 500);")  # Scrolls down 500 pixels
    time.sleep(2)

    try:
        checkout_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@class='btn btn-primary']"))
        )
        checkout_button.click()

    except Exception as e:
        print(f"❌ Checkout button not found. Add product to cart first. Error: {e}")
        return  # Stop execution if checkout can't proceed

    try:
        # ✅ Wait until "Checkout" header appears
        success_message = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//h1[normalize-space()='Checkout']"))
        )

        if success_message.text == "Checkout":
            print("✅ Checkout completed successfully!")

    except Exception as e:
        print(f"❌ Checkout failed. Error: {e}")

# ✅ Run script
driver = login()

if driver:
    add_to_cart(driver)  # ✅ Add products to cart
    checkout(driver)  # ✅ Proceed to checkout

if driver:
    print("✅ Test Completed.")
