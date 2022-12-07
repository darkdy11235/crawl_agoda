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


file = open('.\Data\links1.txt', 'r',encoding="utf8")
links = file.readlines()
class Hotel(object):
    name = ""
    address = ""
    stars = 0
    price = 0
    score = 0
    link = ""
    currency = ""
    images = []
    detail = ""
    facility_highlights = []
    def __init__(self, name = "", address = "", stars = 0, price = 0, score = 0, link = "", currency = "", images = [], detail = "", facility_highlights = []):
        self.name = name
        self.address = address
        self.stars = stars
        self.price = price
        self.score = score
        self.link = link
        self.currency = currency
        self.images = images
        self.detail = detail
        self.facility_highlights = facility_highlights
    def to_dict(self):
        return {
            "name": self.name,
            "address": self.address,
            "stars": self.stars,
            "price": self.price,
            "score": self.score,
            "link": self.link,
            "currency": self.currency,
            "images": self.images,
            "detail": self.detail,
            "facility_highlights": self.facility_highlights
        }


class CrawlHotelListFast():
    hotels = []
    resData = []
    def crawl(self):
        profile_path = r'C:\Users\htk11\AppData\Roaming\Mozilla\Firefox\Profiles\epumps23.default'
        options = Options()
        options.set_preference('profile', profile_path)
        service = Service(r'geckodriver.exe')

        driver = Firefox(service=service, options=options)
        driver.maximize_window()
        loop=0
        for link in links:
            current_window = driver.current_window_handle
            driver.get(link)
            print("loop number-"+str(loop+1))
            loop+=1
            time.sleep(1.5)

            SCROLL_PAUSE_TIME = 0.2
            driver.execute_script("window.scrollBy(0, 1400);")
            time.sleep(SCROLL_PAUSE_TIME)


            try:
                WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, './/h1[@class="HeaderCerebrum__Name"]')))
                hotel_name = driver.find_element(By.XPATH,'.//h1[@class="HeaderCerebrum__Name"]').text
            except:
                hotel_name = ""
            try:
                WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, './/span[@data-selenium="hotel-address-map"]')))
                hotel_address = driver.find_element(By.XPATH,'.//span[@data-selenium="hotel-address-map"]').text
            except:
                hotel_address = ""
            try:
                WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, './/i[@data-selenium="mosaic-hotel-rating"]')))
                hotel_stars = int(driver.find_element(By.XPATH,'.//i[@data-selenium="mosaic-hotel-rating"]').get_attribute("class")[17:18])
            except:
                hotel_stars = 0
            try:
                WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, './/div[@id="hotelNavBar"]//div[@class="Box-sc-kv6pi1-0 hRUYUu StickyNavPrice__priceDetail--lowerText StickyNavPrice__priceDetail--defaultColor"]//span[3]')))
                hotel_price = int(driver.find_element(By.XPATH,'.//div[@id="hotelNavBar"]//div[@class="Box-sc-kv6pi1-0 hRUYUu StickyNavPrice__priceDetail--lowerText StickyNavPrice__priceDetail--defaultColor"]//span[3]').text.replace(".",""))
            except:
                hotel_price = 0
            try:
                WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, './/div[@class="NorthstarSideContent"]//div[@class="Box-sc-kv6pi1-0 ggePrW"]//h3[@class="Typographystyled__TypographyStyled-sc-j18mtu-0 hTkvyT kite-js-Typography "]')))
                hotel_score = float(driver.find_element(By.XPATH,'.//div[@class="NorthstarSideContent"]//div[@class="Box-sc-kv6pi1-0 ggePrW"]//h3[@class="Typographystyled__TypographyStyled-sc-j18mtu-0 hTkvyT kite-js-Typography "]').text.replace(",","."))
            except:
                hotel_score = 0
            try:
                WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, './/div[@id="hotelNavBar"]//div[@class="Box-sc-kv6pi1-0 hRUYUu StickyNavPrice__priceDetail--lowerText StickyNavPrice__priceDetail--defaultColor"]//span[5]')))
                hotel_currency = driver.find_element(By.XPATH,'.//div[@id="hotelNavBar"]//div[@class="Box-sc-kv6pi1-0 hRUYUu StickyNavPrice__priceDetail--lowerText StickyNavPrice__priceDetail--defaultColor"]//span[5]').text
            except:
                hotel_currency = ""
            try:
                WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, './/img[@class="SquareImage"]')))
                hotel_images = driver.find_elements(By.XPATH,'.//img[@class="SquareImage"]')
                hotel_images = [image.get_attribute("src") for image in hotel_images]
            except:
                hotel_images = []
            try:
                WebDriverWait(driver, 2).until(
                    EC.presence_of_element_located((By.XPATH, './/p[@class="Typographystyled__TypographyStyled-sc-j18mtu-0 fHvoAu kite-js-Typography "]')))
                hotel_detail = driver.find_element(By.XPATH,'.//p[@class="Typographystyled__TypographyStyled-sc-j18mtu-0 fHvoAu kite-js-Typography "]').text
            except:
                hotel_detail = ""
            try:
                WebDriverWait(driver, 2).until(
                    EC.presence_of_element_located((By.XPATH,
                                                    './/span[@data-element-name="popular-property-feature"]')))
                hotel_facility_highlights = driver.find_elements(By.XPATH,'.//span[@data-element-name="popular-property-feature"]')
                hotel_facility_highlights = [facility_highlight.text for facility_highlight in hotel_facility_highlights]
            except:
                hotel_facility_highlights = []
            print(hotel_name,hotel_address,hotel_stars,hotel_price,hotel_currency,hotel_score,hotel_images,hotel_detail,hotel_facility_highlights)
            hotel = Hotel(hotel_name, hotel_address, hotel_stars, hotel_price, hotel_score, link, hotel_currency, hotel_images, hotel_detail, hotel_facility_highlights)
            self.hotels.append(hotel)
        driver.quit()
        self.resData = pd.DataFrame([hotel.to_dict() for hotel in self.hotels])
        def export(self, path):
            self.resData.to_csv("path", encoding='utf-8')

firefox_driver_path = '.\Driver\geckodriver.exe' #setup the path of gecko driver
file.close()

#running
cek4 = CrawlHotelListFast() #build the objects
cek4.crawl() #start the crawling process
result = cek4.resData #get the result
result.to_csv("hotels_agoda_danang_"+time.strftime("%Y%m%d-%H%M%S")+".csv", encoding='utf-8') #export the result to csv file
result.to_excel("hotels_agoda_danang_"+time.strftime("%Y%m%d-%H%M%S")+".xlsx") #export the result to excel file
