# Import necessary modules
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time

# Path to the folder where the file will be downloaded
download_folder = "C:\\Users\\omaima\\Desktop\\Data_BI\\transformation_Victims"

# Create the folder if it doesn't exist
if not os.path.exists(download_folder):
    os.makedirs(download_folder)

# Specify the path to the manually downloaded ChromeDriver executable
chrome_driver_path = "C:\\Users\\omaima\\Downloads\\chromedriver.exe"


# Set up Chrome options
chrome_options = Options()
prefs = {"download.default_directory": download_folder}
chrome_options.add_experimental_option("prefs", prefs)

# Set up the Chrome WebDriver
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)


# Navigate to the website
driver.get("https://statistics.btselem.org/en/all-fatalities/by-date-of-incident?section=overall&tab=overview")


try:
    # Wait for the download button to be clickable
    download_button = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "#overall > div > div > div > div:nth-child(1) > div > div.v-card__actions.mt-auto.d-flex.justify-space-between > div:nth-child(2) > button"))
    )

    # Click the download button
    driver.execute_script("arguments[0].click();", download_button)
    print("Button clicked")

    # Wait for the downloaded file to appear in the download folder
    timeout = 30  # Timeout in seconds
    start_time = time.time()
    previous_file_count = len([filename for filename in os.listdir(download_folder) if filename.endswith('.xlsx')])

    while True:
        current_file_count = len([filename for filename in os.listdir(download_folder) if filename.endswith('.xlsx')])

        if current_file_count > previous_file_count:
            print("New file downloaded.")
            break

        if time.time() - start_time > timeout:
            print("Timeout reached. No file downloaded.")
            break

        time.sleep(1)  # Wait for one second

    # Identify the most recent file in the download folder
    latest_file = max([os.path.join(download_folder, f) for f in os.listdir(download_folder)], key=os.path.getctime)

    # Set the new name for the downloaded file
    new_file_name = os.path.join(download_folder,"PK.xlsx")

    # Remove the file if it already exists
    if os.path.exists(new_file_name):
        os.remove(new_file_name)

    # Rename the downloaded file
    os.rename(latest_file, new_file_name)

    print("File renamed and saved as:", new_file_name)

finally:
    # Close the browser
    driver.quit()