import requests
from time import sleep
from typing import List, Union

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def interceptor(request):
    print(request)
    request['User-Agent'] = UserAgent().chrome()

class Item:
    def __init__(self, name:str, price:str, link_to_image:str, link:str, shop:str) -> None:
        self.name = name
        self.price = price
        self.link_to_image = link_to_image
        self.link = link
        self.shop = shop

    def __str__(self) -> str:
        return f'Item Name: {self.name} Price: {self.price} Shop:{self.shop}'

    def __repr__(self) -> str:
        return f'Item Name: {self.name} Price: {self.price} Shop:{self.shop}'


class Shop:
    def __init__(self, name:str, link:str) -> None:
        self.name = name
        self.link = link

    def __str__(self) -> str:
        return f'Shop Name: {self.name}'

    def __repr__(self) -> str:
        return f'Shop Name: {self.name}'

    def get_html(
        self,
        query:str, 
        input_xpath:str,
        scroll:bool=False,
        scroll_timeout:Union[float, int]=0.3,
        time_to_load_main_page:int=2,
        time_to_load_query_request:int=3,):

        driver = webdriver.Chrome(ChromeDriverManager().install())
            
        driver.get(self.link)

        sleep(time_to_load_main_page)

        search_input = driver.find_element(By.XPATH,input_xpath)
        search_input.send_keys(str(query))
        search_input.send_keys(Keys.ENTER)

        sleep(time_to_load_query_request)
        
        if scroll:
            for i in range(5):
                sleep(scroll_timeout)
                driver.execute_script(f"window.scrollTo({i * 300}, {(i+1)*300})") 

        html = driver.page_source
        driver.close()

        return html

    @staticmethod
    def pack_items(
        names:List[str], 
        prices:List[str],
        image_sources:List[str], 
        links:List[str],
        max_items:int,
        source:str) -> List[Item]:
        items = []
        n_items = min(len(names), max_items)

        for i in range(n_items):
            items.append(Item(names[i], prices[i], image_sources[i], links[i], source))
            
        return items      

    def check_availablity(self) -> bool:
        response = requests.get(self.link, timeout=5)
        
        if response.status_code == 200:
            return True
        return False