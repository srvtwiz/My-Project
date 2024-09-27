from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time

website='https://www.redbus.in/'
options = webdriver.ChromeOptions()
options.add_experimental_option("detach",True)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get(website)
time.sleep(4)

# state_name= WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.ID, 'Carousel')))
# data=[]

# for i in state_name:
#     boxes=state_name.find_element(By.CLASS_NAME, 'rtcBack')
#     for name in boxes:
#         data.append(name.text)
#         print(data)

APSRTC_elements = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'rtcBack')))
data=[]

for element in APSRTC_elements:
    element.click()
    driver.back()
    time.sleep(2)