import time
import pandas as pd
import datetime
from selenium import webdriver
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from openpyxl import Workbook

class CrawlHotelListFast():
    links = []
    resData = []
    def crawl(self):
        url = 'https://www.agoda.com/search?city=16440'
        profile_path = r'C:\Users\htk11\AppData\Roaming\Mozilla\Firefox\Profiles\epumps23.default'
        options = Options()
        options.set_preference('profile', profile_path)
        service = Service(r'.\Driver\geckodriver.exe')
        driver = Firefox(service=service, options=options)
        driver.maximize_window()
        driver.get(url)

        current_window = driver.current_window_handle

        for loop in range(0,200):
            print("loop number-"+str(loop+1))
            time.sleep(2)

            SCROLL_PAUSE_TIME = 0.2
            new_height= 0

            # Get scroll height
            last_height = driver.execute_script("return document.body.scrollHeight")

            while True:
                # Scroll down to bottom
                driver.execute_script("window.scrollBy(0, 1000);")
                print(new_height)
                print("-")
                print(last_height)
                # Wait to load page
                time.sleep(SCROLL_PAUSE_TIME)

                # Calculate new scroll height and compare with last scroll height
                new_height = new_height+1000
                if new_height >= last_height:
                    break
                last_height = driver.execute_script("return document.body.scrollHeight")
            #cuoi trang


            ols = driver.find_elements(By.CLASS_NAME,"hotel-list-container")
            for item in ols:
                list_hotels = item.find_elements(By.XPATH,'.//li[@data-selenium="hotel-item"]')
                for hotel_item in list_hotels:
                    # get link
                    try:
                        hotel_link = hotel_item.find_element(By.XPATH,'.//a[@class="PropertyCard__Link"]').get_attribute('href')
                    except:
                        hotel_link = "Unknown"
                    self.links.append(hotel_link)

            try:
                button_next = driver.find_element(By.XPATH,'.//button[@data-selenium="pagination-next-btn"]')
                driver.execute_script("arguments[0].click();", button_next)
            except:
                break
        driver.quit()
        self.resData = self.links
        def export(self, path):
            self.resData

firefox_driver_path = 'geckodriver.exe' #setup the path of gecko driver
output_path = ".\Data\links.txt"


#running
cek4 = CrawlHotelListFast() #build the objects
cek4.crawl() #start the crawling process
result = cek4.resData #get the result
#open the file for write operation
open(output_path , 'w').close()
f = open(output_path , 'w')
#writes the new content
for item in result:
    try:
        f.write(item + "\n")
    except:
        continue
#close the file
f.close()
