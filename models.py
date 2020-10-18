from collections import OrderedDict


class LocationInformationJSON:
    __slots__ = ('address', 'latlon', 'name', 'phones', 'working_hours')

    def __init__(self):
        self.address = self.name = ''
        self.latlon = []
        self.phones = []
        self.working_hours = []

    def convert_to_dict(self):
        return OrderedDict(
            [
                ('address', self.address),
                ('latlon', self.latlon),
                ('name', self.name),
                ('phones', self.phones),
                ('working_hours', self.working_hours)
            ]
        )
