from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
import time

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
wait = WebDriverWait(driver, 30)

#for looping
main_links = {
    'APSRTC': "https://www.redbus.in/online-booking/apsrtc/?utm_source=rtchometile",
    'KSRTC': "https://www.redbus.in/online-booking/ksrtc-kerala/?utm_source=rtchometile",
    'TSRTC': "https://www.redbus.in/online-booking/tsrtc/?utm_source=rtchometile",
    'KTCL': "https://www.redbus.in/online-booking/ktcl/?utm_source=rtchometile",
    'RSRTC': "https://www.redbus.in/online-booking/rsrtc/?utm_source=rtchometile",
    'SBSTC': "https://www.redbus.in/online-booking/south-bengal-state-transport-corporation-sbstc/?utm_source=rtchometile",
    'HRTC': "https://www.redbus.in/online-booking/hrtc/?utm_source=rtchometile",
    'ASTC': "https://www.redbus.in/online-booking/astc/?utm_source=rtchometile",
    'UPSRTC': "https://www.redbus.in/online-booking/uttar-pradesh-state-road-transport-corporation-upsrtc/?utm_source=rtchometile",
    'WBTC': "https://www.redbus.in/online-booking/wbtc-ctc/?utm_source=rtchometile"
}

def scroll():
    last = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(0.2)
        new= driver.execute_script("return document.body.scrollHeight")
        if new == last:
            break
        last = new

def scrape_route_page():
    routes_container = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'route_link')))
    for route in routes_container:
        try:
            link = route.find_element(By.TAG_NAME, 'a')
            route_name = link.get_attribute('title')
            route_link = link.get_attribute('href')
            route_data.append({'route name': route_name, 'route link': route_link})
        except Exception as e:
            print(f"An error: {e}")
            continue

#looping all the state links
for state, state_link in main_links.items():
    driver.get(state_link)
    print(f"Processing state: {state} - {state_link}")
    route_data = []  
    bus_details = []  

#next page
    for page_number in range(1, 10):
        scrape_route_page()

        if page_number < 10:
            try:
                pagination_container = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[4]/div[12]')))
                next_page_button = pagination_container.find_element(By.XPATH, f'.//div[contains(@class, "DC_117_pageTabs") and text()="{page_number + 1}"]')

                actions = ActionChains(driver)
                actions.move_to_element(next_page_button).perform()
                time.sleep(1)
                next_page_button.click()
                wait.until(EC.text_to_be_present_in_element((By.XPATH, '//div[contains(@class, "DC_117_pageTabs DC_117_pageActive")]'), str(page_number + 1)))
                print(f"Current page {page_number + 1}")
                time.sleep(3)

            except Exception as e:
                print(f"An error in page {page_number + 1}: {e}")
                break

#loop for bus routes
    for route in route_data:
        route_name = route['route name']
        route_link = route['route link']
        print(f"Processing {route_name}")
        driver.get(route_link)
        time.sleep(3)

        try:
            view_buses_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "button")))
            driver.execute_script("arguments[0].click();", view_buses_button)
            time.sleep(5)
            scroll()

            bus_page_container = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'clearfix.row-one')))
            bus_name = driver.find_elements(By.CLASS_NAME, 'travels.lh-24.f-bold.d-color')
            bus_type_elements = driver.find_elements(By.CLASS_NAME, "bus-type.f-12.m-top-16.l-color.evBus")
            departure_time = driver.find_elements(By.CLASS_NAME, 'dp-time.f-19.d-color.f-bold')
            arival_time = driver.find_elements(By.CLASS_NAME, 'bp-time.f-19.d-color.disp-Inline')
            rating = driver.find_elements(By.XPATH, "//div[@class='rating-sec lh-24']")
            duration = driver.find_elements(By.CLASS_NAME, 'dur.l-color.lh-24')
            fare = driver.find_elements(By.CLASS_NAME, 'fare.d-block span.f-bold.f-19')
            available_seats = driver.find_elements(By.XPATH, "//div[contains(@class, 'seat-left m-top-30') or contains(@class, 'seat-left m-top-16')]")

            total_buses = max(len(bus_name), len(bus_type_elements), len(departure_time), len(arival_time),len(rating), len(duration), len(fare), len(available_seats))

#loop for bus data
            for i in range(total_buses):
                bus_detail = {
                    "route_name": route_name,
                    "route_link": route_link,
                    "Bus_Name": bus_name[i].text if i < len(bus_name) else "N/A",
                    "Bus_Type": bus_type_elements[i].text if i < len(bus_type_elements) else "N/A",
                    "Departing_Time": departure_time[i].text if i < len(departure_time) else "N/A",
                    "Duration": duration[i].text if i < len(duration) else "N/A",
                    "Reaching_Time": arival_time[i].text if i < len(arival_time) else "N/A",
                    "Star_Rating": rating[i].text if i < len(rating) else "N/A",
                    "Price": fare[i].text if i < len(fare) else "N/A",
                    "Seat_Availability": available_seats[i].text if i < len(available_seats) else "N/A"
                }
                bus_details.append(bus_detail)
                
        except Exception as e:
            print(f"Error for route {route_name}: {e}")

#storing to csv
    df = pd.DataFrame(bus_details)
    df.to_csv(f'{state}_bus_details.csv', index=False)
    print(f"Saved {state}")

driver.quit()
