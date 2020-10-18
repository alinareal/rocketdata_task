import requests

from models import LocationInformationJSON
from utils import create_json


class Parser:

    CITIES_URL = 'https://apigate.tui.ru/api/office/cities'
    CITY_URL_PATTERN = 'https://apigate.tui.ru/api/office/list?cityId={id}'

    def __init__(self):
        self.offices = []

    @staticmethod
    def _get_cities(response):
        cities_info = {}
        cities = response['cities']
        for city_item in cities:
            cities_info[city_item['cityId']] = city_item['name']
        return cities_info

    def run(self, json_name):
        cities = requests.get(self.CITIES_URL).json()
        
        cities_info = self._get_cities(cities)

        for city_id, city_name in cities_info.items():
            city_url = self.CITY_URL_PATTERN.format(id=city_id)
            offices = requests.get(city_url).json()['offices']
            for office in offices:
                json_model = self._fill_json_model(office, city_name)
                self.offices.append(json_model.convert_to_dict())

        create_json(json_name, self.offices)

    @staticmethod
    def _get_address(office, city_name):
        address = office.get('address', '')
        if city_name in address:
            result = address
        else:
            result = ', '.join((city_name, address))
        return result

    def _fill_json_model(self, office, city_name):
        json_model = LocationInformationJSON()
        json_model.address = self._get_address(office, city_name)
        json_model.name = office.get('name', '')
        json_model.latlon.append(office.get('latitude', ''))
        json_model.latlon.append(office.get('longitude', ''))
        json_model.phones.append(office.get('phone', '').split(';'))
        json_model.working_hours = self._get_operation_hours(office)
        return json_model

    @staticmethod
    def _get_hours(operation_time, days_key, days_name):

        off = operation_time.get(days_key, '').get('isDayOff', '')
        if not off:
            start = operation_time.get(days_key, '').get('startStr', '')
            end = operation_time.get(days_key, '').get('endStr', '')
            hours = '{name} {start} до {end}'.format(name=days_name, start=start, end=end)
        else:
            hours = '{name} Выходной'.format(name=days_name)
        return hours

    def _get_operation_hours(self, office):
        operation_time = office.get('hoursOfOperation', '')

        workday_hours = self._get_hours(operation_time, 'workdays', 'пн - пт')
        saturday_hours = self._get_hours(operation_time, 'saturday', 'сб')
        sunday_hours = self._get_hours(operation_time, 'sunday', 'вс')

        return [workday_hours, saturday_hours, sunday_hours]


if __name__ == '__main__':
    parser = Parser()
    parser.run('offices_task2.json')
