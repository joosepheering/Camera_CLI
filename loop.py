from threading import Thread
from src.gps import GPS
from src.db import DB
from src.camera import Camera
from src.ubird import UBird
from subprocess import PIPE, Popen
from time import sleep

CAMERA_NAME = "Sony Alpha-A6000"
PHOTOS_FOLDER = "/Users/roos/Desktop/Pictures/"
CSV_FILE = "/Users/roos/Desktop/gphoto_json/db.csv"
SHOOTING_TIME = 0.1
PROJECT_ID = "99"


def cmdline(command):
    process = Popen(
        args=command,
        stdout=PIPE,
        shell=True
    )
    return process.communicate()[0]


def write_exif(self, picture_path: str, lat: float, lon: float, alt: float):
    if lat > 0:
        lat_m = 'N'
    else:
        lat_m = 'S'
    if lon > 0:
        lon_m = 'E'
    else:
        lon_m = 'W'
    return cmdline(f"exiftool {picture_path} -gpslatitude={lat} -gpslongitude={lon} -gpslatituderef={lat_m}"
                   f" -gpslongituderef={lon_m}")


def start_trigger_timer(seconds):
    sleep(seconds)
    return True


class First(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.gps = GPS()
        self.cam = Camera(CAMERA_NAME, PHOTOS_FOLDER)
        self.daemon = True
        self.start()

    def run(self):
        while True:
            if start_trigger_timer(SHOOTING_TIME):
                print("Take picture")
                cord = self.gps.get_coordinates()
                if self.cam.connect():
                    picture_path = self.cam.capture_photo_and_download()
                    write_exif(picture_path, cord[0], cord[1], cord[2])
                    print(f"Picture taken: {picture_path}")


class Second(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.ubird = UBird(PROJECT_ID)
        self.daemon = True
        self.start()

    def run(self):
        while True:
            print("B")


First()
Second()
while True:
    pass