from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
import time

options = webdriver.ChromeOptions()
options.add_experimental_option("detach",True)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
wait = WebDriverWait(driver, 30) 

main_links=({'APSRTC':"https://www.redbus.in/online-booking/apsrtc/?utm_source=rtchometile",'KSRTC':"https://www.redbus.in/online-booking/ksrtc-kerala/?utm_source=rtchometile",
            'TSRTC ':"https://www.redbus.in/online-booking/tsrtc/?utm_source=rtchometile",'KTCL':"https://www.redbus.in/online-booking/ktcl/?utm_source=rtchometile",
            'RSRTC':"https://www.redbus.in/online-booking/rsrtc/?utm_source=rtchometile",'SBSTC':"https://www.redbus.in/online-booking/south-bengal-state-transport-corporation-sbstc/?utm_source=rtchometile",
            'HRTC':"https://www.redbus.in/online-booking/hrtc/?utm_source=rtchometile",'ASTC':"https://www.redbus.in/online-booking/astc/?utm_source=rtchometile",
            'UPSRTC':"https://www.redbus.in/online-booking/uttar-pradesh-state-road-transport-corporation-upsrtc/?utm_source=rtchometile",'WBTC':"https://www.redbus.in/online-booking/wbtc-ctc/?utm_source=rtchometile"})

for state,state_link in main_links.items():
    driver.get(state_link)
    print(state_link)

    
    route_data = []

    def scrape_route_page():
       
        routes_container = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'route_link')))

        for route in routes_container:
            try:
                link = route.find_element(By.TAG_NAME, 'a')
                route_name= link.get_attribute('title')
                route_link= link.get_attribute('href')

                route_data.append({'route name':route_name,'route link':route_link})

            except Exception as e:
                print(f"An error: {e}")
                continue

for page_number in range(1, 10):
    scrape_route_page()
    if page_number < 10:  
        try:

            pagination_container = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[4]/div[12]')))

            next_page_button = pagination_container.find_element(By.XPATH, f'.//div[contains(@class, "DC_117_pageTabs") and text()="{page_number + 1}"]')

            actions = ActionChains(driver)
            actions.move_to_element(next_page_button).perform()
            time.sleep(1) 

            print(f" page {page_number + 1}")

            next_page_button.click()


            wait.until(EC.text_to_be_present_in_element((By.XPATH, '//div[contains(@class, "DC_117_pageTabs DC_117_pageActive")]'), str(page_number + 1)))

            print(f"current page {page_number + 1}")

            time.sleep(3)
        except Exception as e:
            print(f"An error in page {page_number + 1}: {e}")
            break

  
    for entry in route_data:
        print(entry)
