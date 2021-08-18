from threading import Thread
from src.gps import GPS
from src.camera import Camera
from src.ubird import UBird
from subprocess import PIPE, Popen
from time import sleep
import os
from os.path import isfile, join
import shutil

CAMERA_NAME = "Sony Alpha-A6000"
PHOTOS_FOLDER = "/home/roos/Desktop/Pictures/"
UPLOADED_FOLDER = "home/roos/Desktop/UploadedPictures/"
CSV_FILE = "/Users/roos/Desktop/gphoto_json/db.csv"
SHOOTING_TIME = 0.1
PROJECT_ID = "99"
EXTENSIONS = [".JPEG", ".JPG", "jpg", "jpeg"]


def cmdline(command):
    process = Popen(
        args=command,
        stdout=PIPE,
        shell=True
    )
    return process.communicate()[0]


def write_exif(picture_path: str, lat: float, lon: float):
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


# TODO Get coordinates from gps. Rest of this class works
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
                    print(picture_path)
                    write_exif(picture_path, cord[0], cord[1])
                    print(f"Picture taken: {picture_path}")
                    os.remove(f"{picture_path}_original")


class Second(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.ubird = UBird(PROJECT_ID)
        self.daemon = True
        self.start()

    def run(self):
        while True:
            # TODO Get file names
            onlyfiles = [f for f in os.listdir(PHOTOS_FOLDER) if isfile(join(PHOTOS_FOLDER, f))]
            for file in onlyfiles:
                for ext in EXTENSIONS:
                    if ext in file:
                        # Start uploading image
                        if self.ubird.upload_photo(PHOTOS_FOLDER + file):
                            # Start importing image
                            if self.ubird.import_photo():
                                # Move this photo to another folder
                                shutil.move(PHOTOS_FOLDER + file, UPLOADED_FOLDER)
                                # TODO Check if UPLOADED_FOLDER is full.


First()
Second()
while True:
    pass