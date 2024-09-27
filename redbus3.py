from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 30)  # Increased timeout

driver.get("https://www.redbus.in/online-booking/apsrtc/?utm_source=rtchometile")

#Define a list to store all the route data
all_data = []

def scrape_page():
    # Locate elements  (container)
    routescontainer = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "route_link")))

    # Loop through each route to extract details
    for route in routescontainer:
        try:
            link = route.find_element(By.TAG_NAME, 'a')
            routename= link.get_attribute('title')
            routelink= link.get_attribute('href')

            #Then  Append extracted data to list
            all_data.append({'routename':routename,'routelink':routelink})

        except Exception as e:
            print(f"An error occurred: {e}")
            continue

# Scrape data from the first 5 pages
for page_number in range(1, 6):
    scrape_page()
    if page_number < 5:  # Don't try to click next on the last page
        try:
            # Locate the pagination container
            pagination_container = wait.until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="root"]/div/div[4]/div[12]')
            ))

            # Locate the next page button within the container
            next_page_button = pagination_container.find_element(
                By.XPATH, f'.//div[contains(@class, "DC_117_pageTabs") and text()="{page_number + 1}"]'
            )

            # Ensure the next page button is in view
            actions = ActionChains(driver)
            actions.move_to_element(next_page_button).perform()
            time.sleep(1)  # Wait for a bit after scrolling

            # Log the action
            print(f"Clicking on page {page_number + 1}")

            # Click the next page button
            next_page_button.click()

            # Wait for the page number to update to the next page
            wait.until(EC.text_to_be_present_in_element(
                (By.XPATH, '//div[contains(@class, "DC_117_pageTabs DC_117_pageActive")]'), str(page_number + 1)))

            # Log the successful page navigation
            print(f"Successfully navigated to page {page_number + 1}")

            # Wait for a short duration to ensure the next page loads completely
            time.sleep(3)
        except Exception as e:
            print(f"An error occurred while navigating to page {page_number + 1}: {e}")
            break

# Print the scraped data
for entry in all_data:
    print(entry)