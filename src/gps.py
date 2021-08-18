
import random


class GPS:

    def __init__(self):
        self.lat = 58.0
        self.lon = 25.0
        pass

    def __connect_to_gps(self):
        pass

    def get_coordinates(self):
        lat = float(self.lat + round(random.random(), 4))
        lon = float(self.lon + round(random.random(), 4))
        return [lat, lon]

