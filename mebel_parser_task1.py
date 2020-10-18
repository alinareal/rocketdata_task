import requests
from bs4 import BeautifulSoup

from models import LocationInformationJSON
from utils import create_json


class ShopInformationHTML:
    __slots__ = ('city', 'address', 'latitude', 'longtitude', 'name', 'phones', 'mode1', 'mode2')

    def __init__(self):
        self.city = self.address = self.latitude = self.longtitude = ''
        self.name = self.phones = self.mode1 = self.mode2 = ''


class Parser:

    URL = 'https://www.mebelshara.ru/contacts'
    PARSER = 'html.parser'
    SHOP_PATTERN = 'data-shop-{postfix}'

    def __init__(self):
        self.shops = []

    def run(self, json_name):
        response = requests.get(self.URL)
        content = response.content.decode(response.encoding)

        soup = BeautifulSoup(markup=content, features=self.PARSER)
        city_items = soup.find_all('div', class_='city-item')

        for address in city_items:
            html_model = self._fill_html_model(address)
            json_model = self._fill_json_model(html_model)
            self.shops.append(json_model.convert_to_dict())

        create_json(json_name, self.shops)

    def _fill_html_model(self, item):
        html_model = ShopInformationHTML()
        html_model.city = item.find('h4', class_='js-city-name').text
        shop_item = item.find('div', class_='shop-list-item')
        html_model.address = shop_item.get(self.SHOP_PATTERN.format(postfix='address'), '')
        html_model.latitude = shop_item.get(self.SHOP_PATTERN.format(postfix='latitude'), '')
        html_model.longtitude = shop_item.get(self.SHOP_PATTERN.format(postfix='longitude'), '')
        html_model.name = shop_item.get(self.SHOP_PATTERN.format(postfix='name'), '')
        html_model.phones = shop_item.get(self.SHOP_PATTERN.format(postfix='phone'), '')
        html_model.mode1 = shop_item.get(self.SHOP_PATTERN.format(postfix='mode1'), '')
        html_model.mode2 = shop_item.get(self.SHOP_PATTERN.format(postfix='mode2'), '')
        return html_model

    @staticmethod
    def _fill_json_model(html_model):
        json_model = LocationInformationJSON()
        json_model.address = ', '.join((html_model.city, html_model.address))
        json_model.latlon.append(html_model.latitude)
        json_model.latlon.append(html_model.longtitude)
        json_model.name = html_model.name
        json_model.phones.append(html_model.phones)
        json_model.working_hours.append(' '.join((html_model.mode1, html_model.mode2)))
        return json_model


if __name__ == '__main__':
    parser = Parser()
    parser.run('shops_task1.json')
