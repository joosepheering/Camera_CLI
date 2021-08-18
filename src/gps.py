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
        self.digit = 0.0
        pass

    def __connect_to_gps(self):
        pass

    def get_coordinates(self):
        """
        Get coordinates from GPS, parse it to dict.
        :return: {"lat": -24.0231, "lon": 0.22132}
        """
        self.digit += 0.1
        lat = float(self.lat + self.digit)
        lon = float(self.lon + self.digit)
        alt = float(self.alt + self.digit)
        return [lat, lon, alt]

