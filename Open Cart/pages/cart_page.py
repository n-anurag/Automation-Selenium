from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def add_to_cart(driver):
    """Finds and clicks all 'Add to Cart' buttons."""
    if driver is None:
        print("❌ No valid browser session.")
        return

    # Navigate to homepage to see products
    driver.get("https://demo.opencart.com")

    # ✅ Wait for all "Add to Cart" buttons to appear
    add_to_cart_buttons = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "(//button[@title='Add to Cart'])[1]"))
    )
    driver.execute_script("arguments[0].click();", add_to_cart_buttons)
    # print(f"{len(add_to_cart_buttons)}")

    product_title = driver.find_elements(By.XPATH, "(//div[@class='product-thumb'])")
    print(product_title)

    title = driver.find_element(By.TAG_NAME, "h4").text.strip()
    print(f"{title} is added to cart")
    time.sleep(8)

    # GO to Shopping Cart
    WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//span[normalize-space()='Shopping Cart']")
        )
    ).click()
    time.sleep(5)
