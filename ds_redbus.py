from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

website='https://www.redbus.in/'
options = webdriver.ChromeOptions()
options.add_experimental_option("detach",True)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get(website)
time.sleep(4)
#APSRTC = driver.find_element(By.XPATH,"//div[@class='rtcName']")
APSRTC=driver.find_element(By.CLASS_NAME, 'rtcName')
APSRTC_elements = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'rtcName')))
data=[]
for element in APSRTC_elements:
    data.append(element.text)
df = pd.DataFrame(data, columns=['RTC Name'])
print(df)
#element = driver.find_element(By.NAME, 'APSRTC')
APSRTC.click()
route_1=driver.find_element(By.XPATH,"//a[@href='/bus-tickets/hyderabad-to-vijayawada']")

route_1.click()

