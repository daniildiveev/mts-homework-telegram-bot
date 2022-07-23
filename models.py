import requests

class Item:
    def __init__(self, name:str, price:str, path_to_image:str, link:str) -> None:
        self.name = name
        self.price = price
        self.path_to_image = path_to_image
        self.link = link

    def __str__(self) -> str:
        return f'Item Name: {self.name} Price: {self.price}'


class Shop:
    def __init__(self, name:str, link:str) -> None:
        self.name = name
        self.link = link

    def __str__(self) -> str:
        return f'Shop Name: {self.name}'

    def check_availablity(self) -> bool:
        response = requests.get(self.link)
        
        if response.status_code == 200:
            return True
        return False