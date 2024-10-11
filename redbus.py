from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import pandas as pd

options = webdriver.ChromeOptions()
options.add_experimental_option("detach",True)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
website="https://www.redbus.in/bus-tickets/hyderabad-to-vijayawada?fromCityId=124&toCityId=134&fromCityName=Hyderabad&toCityName=Vijayawada&busType=Any&srcCountry=IND&destCountry=IND&onward=29-Sep-2024"
driver.get(website)
time.sleep(10)
wait = WebDriverWait(driver, 30) 

def scroll():
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        time.sleep(.2)

        new_height = driver.execute_script("return document.body.scrollHeight")


        if new_height == last_height:
            break

        last_height = new_height



try:

    view_buses_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "button")))
    driver.execute_script("arguments[0].click();", view_buses_button)
    time.sleep(5) 
    

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
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
    available_seats =driver.find_elements(By.XPATH, "//div[contains(@class, 'seat-left m-top-30') or contains(@class, 'seat-left m-top-16')]")

    bus_details = []

  
    for i in range(len(bus_page_container)):
        bus_detail = {}

        
        bus_detail["Bus_Name"] = bus_name[i].text if i < len(bus_name) else "N/A"
        bus_detail["Bus_Type"] = bus_type_elements[i].text if i < len(bus_type_elements) else "N/A"
        bus_detail["Departing_Time"] = departure_time[i].text if i < len(departure_time) else "N/A"
        bus_detail["Duration"] = duration[i].text if i < len(duration) else "N/A"
        bus_detail["Reaching_Time"] = arival_time[i].text if i < len(arival_time) else "N/A"
        bus_detail["Star_Rating"] = rating[i].text if i < len(rating) else "N/A"
        bus_detail["Price"] = fare[i].text if i < len(fare) else "N/A"
        bus_detail["Seat_Availability"] = available_seats[i].text if i < len(available_seats) else "N/A"

        bus_details.append(bus_detail)
        print(bus_detail)

except Exception as e:
    print(f"Error occurred: {e}")

for entry in bus_details:
    print(entry)

df = pd.DataFrame(bus_details)

df.to_csv('ap_bus_details.csv', index=False)
