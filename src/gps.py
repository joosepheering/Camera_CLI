"""
GPS handler.

It:
creates connection with Zubax GNSS using usb cable and ros topics,
reads coordinates from Zubax GNSS,
"""
import random


class GPS:

    def __init__(self):
        self.lat = 58.0
        self.lon = 25.0
        self.alt = 15.0
        pass

    def __connect_to_gps(self):
        pass

    def get_coordinates(self):
        """
        Get coordinates from GPS, parse it to dict.
        :return: {"lat": -24.0231, "lon": 0.22132}
        """
        lat = float(self.lat + round(random.random(), 4))
        lon = float(self.lon + round(random.random(), 4))
        alt = float(self.alt + round(random.random(), 4))
        return [lat, lon, alt]

