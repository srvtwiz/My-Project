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
#APSRTC = driver.find_element(By.XPATH,"//div[@class='rtcName']")
#APSRTC=driver.find_element(By.CLASS_NAME, 'rtcName')
APSRTC_elements = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'rtcName')))
data=[]

for element in APSRTC_elements:
    data.append(element.text)
    #time.sleep(4)
    print(data)
    


df = pd.DataFrame(data, columns=['RTC Name'])


# view_all=driver.find_element(By.XPATH,'//*[@id="homeV2-root"]/div[3]/div[1]/div[2]/a')
# view_all.click()
print(df)
count=0
# elements = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, f'//div[@class="rtcName" and text()="TSRTC"]')))
# elements.click()
for i in data:
    count+=1
    elements = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, f'//div[@class="rtcName" and text()="{i}"]')))
    time.sleep(2)
    elements.click()
    driver.back()
    print(i)
    
    
    if count>=2:
        arrow_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "sc-frDJqD")))
        arrow_button.click()


    #elements = driver.find_element(By.XPATH,'//div[@class="rtcName" and text()="{i}"]')
    #elements = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="rtcName" and text()= "{i}"]')))
    #elements.click()
#element = driver.find_element(By.NAME, 'APSRTC')
#APSRTC.click()
#route_1=driver.find_element(By.XPATH,"//a[@href='/bus-tickets/hyderabad-to-vijayawada']")

#route_1.click()
