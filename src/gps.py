"""
GPS handler.

It:
creates connection with Zubax GNSS using usb cable and ros topics,
reads coordinates from Zubax GNSS,
"""


class GPS:

    def __init__(self):
        pass

    def __connect_to_gps(self):
        pass

    def get_coordinates(self) -> dict:
        """
        Get coordinates from GPS, parse it to dict.
        :return: {"lat": -24.0231, "lon": 0.22132}
        """
        return {"lat": 58.6749, "lon": 25.0485, "alt": 15.87}