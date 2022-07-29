from typing import List
from bs4 import BeautifulSoup
from models import Item, Shop

import config as cfg


class MvideoParser(Shop):
    def __init__(self):
        Shop.__init__(self, 'Mvideo', 'https://www.mvideo.ru')

    def parse(self, query:str, max_items:int=5) -> List[Item]:
        if not query:
            raise ValueError("query cannot be empty")

        html = self.get_html(input_xpath='//*[@id="1"]', query=query)
        soup = BeautifulSoup(html, 'html.parser')

        a_elements = soup.find_all('a', {'class':'product-title__text'})
        links = [self.link + element['href'] for element in a_elements]
        names = [element.text.replace('\xa0', '') for element in a_elements]

        spans = soup.find_all('span', {'class':'price__main-value'})
        prices = [span.text.replace('\xa0', '') for span in spans]

        images = soup.find_all('img', {'class':'product-picture__img'})
        image_sources = ['https:' + image['src'] for image in images]

        for img_src in image_sources:
            img_src = img_src[:-4]


        return self.pack_items(names, prices, image_sources, links, max_items, cfg.MVIDEO)


class TeknoparkParser(Shop):
    def __init__(self):
        Shop.__init__(self, 'Teknopark', 'https://www.technopark.ru')

    def parse(self, query:str, max_items:int=5) -> List[Item]:
        if not query:
            raise ValueError("query cannot be empty")

        url = self.link + '/search/?q='

        for token in query.split():
            url += f'{token}%20'

        html = self.get_html(input_xpath='//*[@id="header-search-input-main"]', query=query, scroll=True)
        soup = BeautifulSoup(html, 'html.parser')
        print()

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

        return self.pack_items(names, prices, image_sources, links, max_items, cfg.TEKNOPARK)