import requests
import os
from time import sleep

from bs4 import BeautifulSoup
import selenium
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import config as cfg
from models import Item, Shop

def parse_ozon(query:str) -> tuple:
    raise NotImplementedError


def parse_wb(query:str, num_items_to_find:int=2) -> tuple:
    '''
    Function to parse image, name and price of an item from wildberries.ru
    query: name of item
    num_items_to_find: number of items we want to process on web page
    '''
    url = 'https://www.wildberries.ru/'

    driver = selenium.webdriver.Chrome(ChromeDriverManager().install())
    driver.get(url)

    sleep(2)

    search_input = driver.find_element(By.XPATH,'//*[@id="searchInput"]')
    search_input.send_keys(str(query))
    search_input.send_keys(Keys.ENTER)

    sleep(2)

    html = driver.page_source
    driver.close()

    soup = BeautifulSoup(html, 'html.parser')

    product_cart_list = soup.find_all('div', {'class':'product-card-list'})
    soup = BeautifulSoup(str(product_cart_list), 'html.parser')

    a_elements = soup.find_all('a', {'class':'product-card__main'})
    links = [element.href for element in a_elements][:num_items_to_find]

    product_divs = soup.find_all('span', {'class' : 'lower-price'})
    prices = [element.text.strip() for element in product_divs][:num_items_to_find]

    images = soup.find_all('div', {'class':'j-thumbnail'})
    image_links = [element.src for element in images]



def parse_mvideo(query:str) -> tuple:
    raise NotImplementedError


def parse_all(query:str) -> tuple:
    raise NotImplementedError

if __name__ == '__main__':
    parse_wb('iphone 13')

    #//*[@id="c40652656"]/div
    #//*[@id="c40654196"]/div