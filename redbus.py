from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time

website='https://www.redbus.in'
options = webdriver.ChromeOptions()
options.add_experimental_option("detach",True)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get(website)
wait = WebDriverWait(driver, 10)


page = 1
all_route = []
route_name=[]
route_link=[]
while True:
    print(f"Processing page {page}")

    # Re-acquire the nested div after navigating to the next page
    nested_div = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="Carousel"]')))

    # Find route links on the current page and collect them
    route_links = nested_div.find_elements(By.CSS_SELECTOR, 'div.rtcBack')

    all_route.extend(route_links)

    break


for route in all_route:
    link = route.find_element(By.TAG_NAME, 'a')
    route_name = link.get_attribute('title')
    #route_link = link.get_attribute('href')
    print(route_name)

driver.quit()

# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import time

# # Initialize the Chrome driver
# driver = webdriver.Chrome()

# # Open the RedBus website
# driver.get("https://www.redbus.in/online-booking/ksrtc-kerala/?utm_source=rtchometile")

# wait = WebDriverWait(driver, 10)

# # Wait until the nested div is present
# nested_div = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.D117_main.D117_container')))

# page = 1
# all_route = []

# while True:
#     print(f"Processing page {page}")

#     # Re-acquire the nested div after navigating to the next page
#     nested_div = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.D117_main.D117_container')))

#     # Find route links on the current page and collect them
#     route_links = nested_div.find_elements(By.CSS_SELECTOR, 'div.route_link')

#     all_route.extend(route_links)

#     break

# for route in all_route:
#     link = route.find_element(By.TAG_NAME, 'a')
#     route_name = link.get_attribute('title')
#     route_link = link.get_attribute('href')
#     print(route_name,route_link)