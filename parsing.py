from typing import List, Union
from bs4 import BeautifulSoup
from models import Item, Shop
import config as cfg


class MvideoParser(Shop):
    def __init__(self):
        Shop.__init__(self, 'Mvideo', 'https://www.mvideo.ru')

    def parse(self, query:str, max_items:int=5, results:list=[], return_items:bool=True) -> Union[None, List[Item]]:
        if not query:
            raise ValueError("query cannot be empty")

        html = self.get_html(input_xpath='//*[@id="1"]', query=query)
        soup = BeautifulSoup(html, 'html.parser')

        a_elements = soup.find_all('a', {'class':'product-title__text'})
        links = [self.link + element['href'] for element in a_elements]
        names = [element.text.replace('\xa0', '') for element in a_elements]

        spans = soup.find_all('span', {'class':'price__main-value'})
        prices = [span.text.replace('\xa0', '') for span in spans]

        a_image_elements = soup.find_all('a', {'class':'product-picture-link'})
        images = []

        for a_el in a_image_elements:
            image_soup = BeautifulSoup(str(a_el), 'html.parser')
            images.append(image_soup.find('img', {'class':'product-picture__img'}))

        image_sources = ['https:' + image['src'] for image in images]

        items = self.pack_items(names, prices, image_sources, links, max_items, cfg.MVIDEO)

        if return_items:
            return items
        else:
            results += items


class TeknoparkParser(Shop):
    def __init__(self):
        Shop.__init__(self, 'Teknopark', 'https://www.technopark.ru')

    def parse(self, query:str, max_items:int=5, results:list=[], return_items:bool=True) -> Union[None, List[Item]]:
        if not query:
            raise ValueError("query cannot be empty")

        html = self.get_html(input_xpath='//*[@id="header-search-input-main"]', query=query, scroll=True)
        soup = BeautifulSoup(html, 'html.parser')

        image_divs = soup.find_all('div', {'class':'card-listing__image'})
        div_soup = BeautifulSoup(str(image_divs), 'html.parser')
        image_elements = div_soup.find_all('img')
        image_sources = [image_element['data-src'] for image_element in image_elements]

        names_elements = soup.find_all('div', {'class':'card-listing__name'})
        names = [name_element.text for name_element in names_elements]

        a_elements = soup.find_all('a', {'class' : 'card-listing__title'})
        links = [self.link + a_element['href'] for a_element in a_elements]

        price_elements = soup.find_all('span', {'class':'price'})
        prices = [price_element.text for price_element in price_elements]

        if return_items:
            return self.pack_items(names, prices, image_sources, links, max_items, cfg.TEKNOPARK)
        else:
           results += self.pack_items(names, prices, image_sources, links, max_items, cfg.TEKNOPARK)