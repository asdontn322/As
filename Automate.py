import logging
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Constants
LOG_FILE = "logs/automation.log"

# Setup logging
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def init_browser(download_dir):
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "safebrowsing.enabled": True
    })
    return webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

def download_excel(url, download_dir):
    driver = init_browser(download_dir)
    try:
        logging.info(f"Navigating to {url}")
        driver.get(url)

        wait = WebDriverWait(driver, 15)

        # Click "View in Excel"
        view_excel = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "View in Excel")))
        view_excel.click()
        time.sleep(3)

        # Switch to popup window or dialog
        driver.switch_to.window(driver.window_handles[-1])

        # Select Excel 2000 radio button
        excel_option = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='radio' and contains(@value,'Excel')]")))
        excel_option.click()

        # Click OK button to download
        ok_btn = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Ok")))
        ok_btn.click()

        logging.info("Waiting for download to complete...")
        time.sleep(15)
        logging.info("Excel file downloaded successfully.")

    except Exception as e:
        logging.error(f"Automation failed: {str(e)}")
    finally:
        driver.quit()

if __name__ == "__main__":
    print("=== eTracker Excel Automation ===")
    url = input("Enter the eTracker project URL: ")
    download_dir = input("Enter full path to download folder: ")

    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    logging.info("Automation started.")
    download_excel(url, download_dir)
    logging.info("Automation completed.")
