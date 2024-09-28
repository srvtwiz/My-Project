from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 30) 
options = webdriver.ChromeOptions()
options.add_experimental_option("detach",True)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
website="https://www.redbus.in/bus-tickets/hyderabad-to-vijayawada?fromCityId=124&toCityId=134&fromCityName=Hyderabad&toCityName=Vijayawada&busType=Any&srcCountry=IND&destCountry=IND&onward=29-Sep-2024"
driver.get(website)
time.sleep(10)
bus_data = ({})
bus_page_container=wait.until(EC.presence_of_element_located((By.CLASS_NAME,'result-sec')))
bus_details_container=bus_page_container.find_elements(By.CLASS_NAME,'clearfix bus-item-details')
for bus in bus_details_container:
    try:
          # Extract the bus name
        bus_name = bus.find_element(By.CLASS_NAME, 'travels').text

        # Extract departure time
        departure_time = bus.find_element(By.CLASS_NAME, 'dp-time').text

        # Extract the rating
        rating = bus.find_element(By.CLASS_NAME, 'rating').text

        # Extract the journey duration
        duration = bus.find_element(By.CLASS_NAME, 'dur').text

        # Extract the fare
        fare = bus.find_element(By.CLASS_NAME, 'fare').text

        # Extract available seats
        available_seats = bus.find_element(By.CLASS_NAME, 'seat-left').text

        bus_data.append({'bus_name': bus_name,'departure_time': departure_time,'rating': rating,'duration': duration,'fare': fare,'available_seats': available_seats})
    except Exception as e:
        print(f"Error occurred: {e}")
        continue
for entry in bus_data:
    print(entry)