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
# Get the current date and time
now = datetime.datetime.now()

# Format the date and time as a string
date_string = now.strftime("%Y-%m-%d")
time_string = now.strftime("%H:%M:%S")

message = f"\nDATETIME {date_string} {time_string}" \
          f"\n[Mercedes Crawler]" \
          f"\n\n"

# navigate to the desired page
mercedes = 'https://shop.mercedes-benz.com/ko-kr/shop/vehicle/srp/used?sort=price-asc&assortment=vehicle&priceSlider' \
           '=37000000&fuel_type=BENSIN&mileageSlider=50000&model=C-CLASS&model=CLA&model=GLA '


class Car:
    def __init__(self, title, price, date, link, address):
        self.title = title
        self.price = price
        self.date = date
        self.link = link
        self.address = address

    def __str__(self):
        return f"==========\n" \
               f"차종: {self.title}\n" \
               f"가격: {self.price},\n" \
               f"연식/ 주행거리/ 연료: {self.date}\n" \
               f"링크: https://shop.mercedes-benz.com{self.link}\n" \
               f"주소: {self.address}" \
               f"\n\n"


driver.get(mercedes)
time.sleep(20)

# extract the HTML content of the page
html = driver.page_source

# parse the HTML using BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')

# Extract the text inside the string tag with class name "dcp-cars-product-tile__model"
titles = soup.find_all('strong', {'class': 'dcp-cars-product-tile__model'})
prices = soup.find_all('p', {'class': 'dcp-product-tile-highlight-label'})
info = soup.find_all('div', {'class': 'dcp-product-tile-used-car-info'})
link_div = soup.find_all('div', {'class': 'dcp-image-slider dcp-cars-product-tile__image'})
dealer = soup.find_all('span', {'class': 'dcp-cars-product-tile-dealer__address'})

message += f"\n검색 결과 : {len(titles)}\n"

for i in range(len(titles)):
    car = Car(titles[i].text.strip(),
              prices[i].text.strip().removesuffix("  [4]  (VAT 포함)"),
              info[i].text.strip(),
              link_div[i].find('a')["href"],
              dealer[i].text.strip())
    message += f"[{i+1}] "
    message += car.__str__()

if not message:
    message += "No Results"
# close the webdriver


# Access the environment variables
load_dotenv()  # Load environment variables from .env file
token = os.getenv("TOKEN")
chat_id = os.getenv("CHAT_ID")
url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={message}"

requests.get(url).json()  # this sends the message
driver.quit()  # shut down the browser
