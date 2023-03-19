import datetime
import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv
import os

chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)


class Car:
    def __init__(self, title, price, date, link):
        self.title = title
        self.price = price
        self.date = date
        self.link = link

    def __str__(self):
        return f"==========\n" \
               f"차종: {self.title}\n" \
               f"가격: {self.price},\n" \
               f"연식/ 주행거리/ 연료: {self.date}\n" \
               f"링크: https://shop.mercedes-benz.com{self.link}" \
               f"\n==========\n"


def get_cars():
    # Get the current date and time
    now = datetime.datetime.now()

    # Format the date and time as a string
    date_string = now.strftime("%Y-%m-%d")
    time_string = now.strftime("%H:%M:%S")

    message = f"===" \
              f"\nDATETIME {date_string} {time_string}" \
              f"\n[Mercedes Crawler]" \
              f"\n===" \
              f"\n\n"

    # navigate to the desired page
    url = 'https://shop.mercedes-benz.com/ko-kr/shop/vehicle/srp/used?sort=relevance' \
          '&assortment=vehicle' \
          '&priceSlider=37000000' \
          '&model=C-CLASS' \
          '&bodyType=LIMOUSINE' \
          '&fuel_type=BENSIN' \
          '&mileageSlider=40000'

    driver.get(url)
    time.sleep(20)

    # extract the HTML content of the page
    html = driver.page_source

    if "maintenance" in html:
        message += "Webpage is under maintenance"
    else:
        # parse the HTML using BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')

        # Extract the text inside the string tag with class name "dcp-cars-product-tile__model"
        titles = soup.find_all('strong', {'class': 'dcp-cars-product-tile__model'})
        prices = soup.find_all('p', {'class': 'dcp-product-tile-highlight-label'})
        info = soup.find_all('div', {'class': 'dcp-product-tile-used-car-info'})
        link_div = soup.find_all('div', {'class': 'dcp-image-slider dcp-cars-product-tile__image'})

        for i in range(len(titles)):
            car = Car(titles[i].text.strip(), prices[i].text.strip().removesuffix("  [4]  (VAT 포함)"),
                      info[i].text.strip(),
                      link_div[i].find('a')["href"])
            message += car.__str__()

        if not message:
            message += "list is empty"
        # close the webdriver

    driver.quit()
    # Access the environment variables
    token = os.getenv("TOKEN")
    chat_id = os.getenv("CHAT_ID")
    url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={message}"
    requests.get(url).json()  # this sends the message


load_dotenv()  # Load environment variables from .env file
get_cars()
