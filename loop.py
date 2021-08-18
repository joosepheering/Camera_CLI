from threading import Thread
from subprocess import PIPE, Popen
from datetime import datetime
from time import sleep
from pathlib import Path
from os.path import isfile, join
import signal
import shutil
import random
import os

CAMERA_NAME = "Sony Alpha-A6000"
GPHOTO_PROCESS_NAME = "gphoto2"
PHOTOS_FOLDER = f"{Path.home()}/Desktop/Pictures/"
UPLOADED_FOLDER = f"{Path.home()}/Desktop/Uploaded/"
SHOOTING_TIME = 0.1
PROJECT_ID = "99"
POWER_LINE_NAME = "Demo"
EXTENSIONS = [".JPEG", ".JPG", "jpg", "jpeg", ".png", ".PNG"]
TOKEN = ""


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


class Camera:

    def __init__(self, camera_name: str, folder_to_store: str):
        self.camera_name = camera_name
        self.folder_to_store = folder_to_store

    def connect(self) -> bool:
        while True:
            if self.__is_connected():
                print("Camera is connected")
                return True
            else:
                self.__kill_gphoto2_process()
                print("Camera not connected. Killing gphoto2 process.")

    def __is_connected(self) -> bool:
        if self.camera_name in str(cmdline("gphoto2 --auto-detect")):
            return True
        else:
            return False

    def __kill_gphoto2_process(self):
        for line in cmdline("ps -A").splitlines():
            if GPHOTO_PROCESS_NAME in str(line):
                # Kill the process
                pid = int(line.split(None, 1)[0])
                os.kill(pid, signal.SIGKILL)

    def __get_new_image_name(self) -> str:
        return f"{self.folder_to_store}{datetime.now().strftime('%Y-%m-%d-%H:%M:%S')}.jpg"

    def __clear_camera_memory(self):
        # TODO Run gphoto2 --list-files when you have inserted memory card. If it causes trouble,
        #   create variable to store filepath name {} and uncomment next line
        # cmdline(f"gphoto2 --folder {SD_CARD_FOLDER} -R --delete-all-files")
        pass

    def capture_photo_and_download(self) -> str:
        self.__kill_gphoto2_process()
        image_path = self.__get_new_image_name()
        cmdline(f"gphoto2 --capture-image-and-download --filename {image_path}")
        sleep(0.5)
        return image_path


class UBird:

    def __init__(self, project_id: str, power_line_name: str):
        self.project_id = project_id
        self.power_line_name = power_line_name
        pass

    def upload_photo(self, photo_path: str):
        return cmdline(f'curl -X POST "https://api.ubird.wtf/ubird/upload/project/{self.project_id}/pictures" -H "accept: */*" -H "Content-Type: multipart/form-data" -H "Authorization: Bearer {TOKEN}" -F "file=@{photo_path};type=image/jpeg"')

    def import_photo(self):
        lat1 = 89.9
        lon1 = -179.9
        lat2 = -89.9
        lon2 = 179.9
        return cmdline(f'curl -X POST "https://api.ubird.wtf/ubird/jobs/project/{self.project_id}/uploads/{lat1}/{lon1}/{lat2}/{lon2}/start?powerLineName={self.power_line_name}" -H "accept: application/json" -H "Authorization: Bearer {TOKEN}"')


# TODO Get coordinates from gps. Rest of this class works
class CameraThread(Thread):
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


class UploadThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.ubird = UBird(PROJECT_ID, POWER_LINE_NAME)
        self.daemon = True
        self.start()

    def run(self):
        while True:
            files = [f for f in os.listdir(PHOTOS_FOLDER) if isfile(join(PHOTOS_FOLDER, f))]
            if len(files) > 0:
                for file in files:
                    for ext in EXTENSIONS:
                        if ext in file:
                            # Start uploading image
                            if self.ubird.upload_photo(PHOTOS_FOLDER + file):
                                # Start importing image
                                if self.ubird.import_photo():
                                    # Move this photo to another folder
                                    shutil.move(PHOTOS_FOLDER + file, UPLOADED_FOLDER)
                                    # TODO Check if UPLOADED_FOLDER is full.


if __name__ == "__main__":

    # TODO Read user input for TOKEN, Project_ID and power line name
    CameraThread()
    UploadThread()
    while True:
        pass
