from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.common.exceptions import TimeoutException
import pandas as pd
import time


options = webdriver.ChromeOptions()
options.add_experimental_option("detach",True)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


wait = WebDriverWait(driver, 10)


# Initialize the Chrome driver


# Open the RedBus website
driver.get("https://www.redbus.in/online-booking/ksrtc-kerala/?utm_source=rtchometile")
driver.maximize_window() 

# Wait until the nested div is present
nested_div = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.D117_main.D117_container')))

page = 1

while True:
    try:
        # Find elements you want to scrape on the current page
        route_links = nested_div.find_elements(By.CSS_SELECTOR, 'div.route_link')
        for route in route_links:
            link = route.find_element(By.TAG_NAME, 'a')
            route_name = link.get_attribute('title')
            route_link = link.get_attribute('href')
            print(route_name,route_link)
            page_tabs = driver.find_elements(By.CLASS_NAME, "DC_117_pageTabs ")
        for i in range(len(page_tabs)):
            if i > 0:
                page_tabs = driver.find_elements(By.CLASS_NAME, "DC_117_pageTabs ")[i]
                driver.execute_script("arguments[0].click();", page_tabs)
                time.sleep(4)
    
        
        
        

        
        # while True:
        #     try:
        #         # Check if the Next button is clickable
        #         next_button1 = wait.until(EC.presence_of_element_located(By.XPATH, '//*[@id="root"]/div/div[4]/div[12]/div[2]'))
        #         next_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div[4]/div[12]/div[2]')))
        #         print("Next button is found and clickable")
        #         break  # Exit the loop if the Next button is found
        #     except:
        #         # Scroll down the page if the Next button is not visible yet
        #         driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
        #         time.sleep(1)  # Wait a bit for the page to load
        # Locate the "Next" button
        
        # Click the "Next" button
        

        # Optional: wait for the next page to load (depending on the site's behavior)
        #wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'your_element_selector')))

    except (NoSuchElementException, TimeoutException):
        print("No more pages to navigate.")
        break

page_tabs = driver.find_elements(By.CLASS_NAME, "DC_117_pageTabs ")
for i in range(len(page_tabs)):
    if i > 0:
        page_tabs = driver.find_elements(By.CLASS_NAME, "DC_117_pageTabs ")[i]
        driver.execute_script("arguments[0].click();", page_tabs)
        time.sleep(4)
    
driver.quit()

# while True:
#     print(f"Processing page {page}")

#     # Re-acquire the nested div after navigating to the next page
#     #nested_div = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.D117_main.D117_container')))

#     # Find route links on the current page and collect them
#     route_links = driver.find_elements(By.CSS_SELECTOR, 'div.route_link')

    

#     break

# for route in route_links:
#     link = route.find_element(By.TAG_NAME, 'a')
#     route_name = link.get_attribute('title')
#     route_link = link.get_attribute('href')
#     print(route_name,route_link)
































# #to view all the states
# View_all_state=driver.find_element(By.XPATH, '//*[@id="homeV2-root"]/div[3]/div[1]/div[2]/a')
# View_all_state.click()
# time.sleep(3)
# count=0
# # states_main=driver.find_element(By.CLASS_NAME, 'D113_ul_rtc')
# states=driver.find_elements(By.CSS_SELECTOR, 'li.D113_item_rtc')

# try:
#     # states_main=wait.until(EC.presence_of_all_elements_located((By.XPATH,'//*[@id="root"]/div/article[2]/div/div')))
#     # states=states_main.find_elements(By.CSS_SELECTOR, 'li.D113_item_rtc')


#     for state in states:
#         count+=1
#         print(count)
#         if count<10:
#             link=state.find_element(By.TAG_NAME, 'a')
#             state_name=link.get_attribute('title')
#             state_link=link.get_attribute('href')
#             print(state_name,state_link)
# except TimeoutException:
#     print("Elements not found in the allotted time")



