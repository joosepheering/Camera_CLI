from threading import Thread
from subprocess import PIPE, Popen
from datetime import datetime
from time import sleep
from pathlib import Path
from os.path import isfile, join
import getopt
import serial
import signal
import shutil
import sys
import os

CAMERA_NAME = "Sony Alpha-A6000"
GPHOTO_PROCESS_NAME = "gphoto2"
PHOTOS_FOLDER = f"{Path.home()}/Desktop/Pictures/"
UPLOADED_FOLDER = f"{Path.home()}/Desktop/Uploaded/"
SHOOTING_TIME = 0.1
EXTENSIONS = [".JPEG", ".JPG", "jpg", "jpeg", ".png", ".PNG"]
GPS_PATH = ""               # "/dev/cu.usbmodem141401"
PROJECT_ID = ""             # 99
POWER_LINE_NAME = ""        # Demo
TOKEN = ""                  # sdsffieo98788yf34h98


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
        self.ser = serial.Serial(GPS_PATH, 9600, timeout=5.0)

    def get_coordinates(self):
        x = str(self.ser.read(1200))
        pos1 = x.find("$GPRMC")
        pos2 = x.find("\n", pos1)
        loc = x[pos1:pos2]
        data = loc.split(',')

        if data[2] == 'V':
            print('No GPS lock')
            return [0.0, 0.0, False]
        else:
            latitude = data[3]
            lat_pointer = latitude.find(".")
            lat_deg = float(latitude[:lat_pointer - 2])
            lat_min = float(latitude[lat_pointer - 2:]) / 60
            latitude = lat_deg + lat_min

            longitude = data[5]
            lon_pointer = longitude.find(".")
            lon_deg = float(longitude[:lon_pointer - 2])
            lon_min = float(longitude[lon_pointer - 2:]) / 60
            longitude = lon_deg + lon_min

            return [latitude, longitude, True]


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
                sleep(1)

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


class CameraThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.gps = GPS()
        self.cam = Camera(CAMERA_NAME, PHOTOS_FOLDER)
        self.daemon = True
        self.start()

    def run(self):
        while True:
            try:
                if start_trigger_timer(SHOOTING_TIME):
                    cord = self.gps.get_coordinates()
                    # IF GPS has lock
                    # if cord[2]:
                        # IF Camera is connected
                    if self.cam.connect():
                        print("Take picture")
                        picture_path = self.cam.capture_photo_and_download()
                        print(picture_path)
                        write_exif(picture_path, cord[0], cord[1])
                        sleep(1)
                        print(f"Picture taken: {picture_path}")
                        os.remove(f"{picture_path}_original")
            except Exception as e:
                print(e)


class UploadThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.ubird = UBird(PROJECT_ID, POWER_LINE_NAME)
        self.daemon = True
        self.start()

    def run(self):
        while True:
            try:
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
            except Exception as e:
                print(e)


if __name__ == "__main__":

    argv = sys.argv[1:]
    got_correct_arguments = False

    def show_options():
        print('ALL THESE OPTIONS ARE REQUIRED:')
        print("-g <gps_serial_path>  = '/dev/cu.usbmodem141401' ")
        print("-p <project_id>  = 99")
        print("-l <power_line_name> == Demo")
        print("-t <token> == fdkmfslkmnfenklfm")

    try:
        opts, args = getopt.getopt(argv, "hg:p:l:t:", ["gps_serial_path=", "project_id=", "power_line_name=", "token="])
    except getopt.GetoptError:
        show_options()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            show_options()
            sys.exit()
        elif opt in ("-g", "--gps_serial_path"):
            GPS_PATH = str(arg).strip().replace('"', "")
        elif opt in ("-p", "--project_id"):
            PROJECT_ID = arg
        elif opt in ("-l", "--power_line_name"):
            POWER_LINE_NAME = arg
        elif opt in ("-t", "--token"):
            TOKEN = str(arg).strip().replace('"\'', "")

    if len(argv) >= 8:
        CameraThread()
        UploadThread()
        while True:
            pass
    else:
        show_options()
