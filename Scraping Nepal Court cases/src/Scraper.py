#  Automating Case Scraping


from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import csv
from bs4 import BeautifulSoup
court_list = [
#     {
#         "court_name": "Supreme Court",
#         "URL": "https://supremecourt.gov.np/lic/sys.php?d=reports&f=weekly_public",
#         "xpath_search_case": "//input[@value='SEARCH']",
#         "bs4_case_selector": "tr td:nth-of-type(5), tr td:nth-of-type(5) br",  # - Capture multi-line case number
#         "scraper_type":"bs4"
#     },
#  {
#         "court_name": "Special Court",
#         "URL": "https://supremecourt.gov.np/special/syspublic.php?d=reports&f=weekly_public",
#         "xpath_search_case": "//input[@name='submit']",
#         "xpath_cases": "//td[contains(text(), '-CR-')]", 
#         "scraper_type":"selenium",  
#  },
    {
        "court_name": "Debt Revenue Court",
        "URL": "https://drtribunal.gov.np/app/weekly",
        "xpath_search_case": "//span[@class='px-3']",
        "bs4_case_selector": "tr td a",
        "scraper_type":"bs4"
    }

]


def bs4_scraper(driver,court):

    # scrape each case number in text format
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    case_numbers = [td.text.strip() for td in soup.select(court["bs4_case_selector"]) if td.text.strip()]
    return case_numbers
    return driver

def selenium_scraper(driver,court) :

    case_elements = driver.find_elements(By.XPATH, court["xpath_cases"])
    case_numbers = [case.text.strip() for case in case_elements if case.text.strip()]
    return case_numbers
    return driver

def scrape_cases(return_only_cases=False):
    driver = webdriver.Chrome()
    all_cases = []  # - Store cases with court names (for CSV)
    case_numbers_only = []  # Store only case numbers 

    for court in court_list:
        driver.get(court['URL'])

        # Click on search button
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, court["xpath_search_case"]))
        ).click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//tbody"))
        )

        # Scrape cases 
        if court["scraper_type"] == "selenium":
            case_numbers = selenium_scraper(driver, court)
        elif "bs4_case_selector" in court:
            case_numbers = bs4_scraper(driver, court)
        else:
            print(f"⚠ Skipping {court['court_name']} - No valid selector found.")
            case_numbers = []

        print(f"{court['court_name']}: {len(case_numbers)} cases found")

        # - Store cases with court names for CSV
        all_cases.extend([(court["court_name"], case) for case in case_numbers])

        # - Store only case numbers
        case_numbers_only.extend(case_numbers)

    driver.quit()


    return case_numbers_only if return_only_cases else all_cases
   
   
# save cases to csv file
def save_to_csv(data):
    with open("scraped_cases.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Court Name", "Case Number"])  # CSV Header
        writer.writerows(data)
    print("Data saved to scraped_cases.csv")

# Add to csv file
# scraped_cases = scrape_cases()
# save_to_csv(scraped_cases)