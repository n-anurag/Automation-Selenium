from selenium import webdriver
from selenium.webdriver.common.by import By
import time


driver = webdriver.Firefox()
query = "laptop"
file = 0
for i in range(1,10):
    driver.get(f"https://www.amazon.in/s?k={query}&page={i}&crid=39AK7IU7KQ02T&sprefix=lapto%2Caps%2C278&ref=nb_sb_noss_2")


    elems= driver.find_elements(By.CLASS_NAME, "puis-card-container")
    print(f"{len(elems)} items found" )
    for elem in elems:
        d = elem.get_attribute("outerHTML")
        with open(f"data/{query}__{file}.html","w",encoding="utf-8") as f:
            f.write(d)
        file += 1




    # time.sleep(5)
driver.quit()
