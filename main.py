"""
Main program of ubird uploader program.

It:
decides when to trigger,
receives coordinates from gps_handler,
sends capture command to camera, receives new picture path,
writes coordinates to exif,
commands picture to be uploaded to ubird,
commands picture to be imported to ubird
creates buffer file to compare uploaded picture names and to be uploaded picture names,
creates threads for different handlers,
"""
from src.gps import GPS
from src.db import DB
from src.camera import Camera
from src.ubird import UBird
from subprocess import PIPE, Popen
from time import sleep
import concurrent.futures

CAMERA_NAME = "Sony Alpha-A6000"
PHOTOS_FOLDER = "/Users/roos/Desktop/Pictures/"
CSV_FILE = "/Users/roos/Desktop/gphoto_json/db.csv"
SHOOTING_TIME = 0.1


def cmdline(command):
    process = Popen(
        args=command,
        stdout=PIPE,
        shell=True
    )
    return process.communicate()[0]


class Main:

    def __init__(self):
        self.gps = GPS()
        self.db = DB(CSV_FILE)
        self.cam = Camera(CAMERA_NAME, PHOTOS_FOLDER)
        # self.ubird = UBird
        # self.ubird.authenticate()

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

    def run(self):
        # 1. Thread
        """ Make a picture command"""
        # 2. Thread
        """
        Make a picture command
        Make sure camera is connected
        Get coordinates
        Trigger camera -> 2. Thread -> Receive input file name.
        When input file name, Write exif
        Make checksum
        Write json file new line with "uploaded" == false.
        Run 2. Thread instance
        """
        # 3. Thread
        """
        Loop through json file, search for "uploaded" == false file. - open json file as lines. for line in lines:
            GET_is_picture_uploaded. Ask Picture by checksum. Check if it has been uploaded
                IF TRUE:
                    IF Read from json, if it "imported" == False:
                        IF import() == True:
                        Start from beginning. Pass
                ELSE:
                    upload to ubird
                        IF return == 200:
                            change json "uploaded" == True
                            import to ubird
                                IF return == 200:
                                    change json "imported" == True
                                ELSE:
        """
        pictures_list = ['DSC00323.JPG', 'DSC00324.JPG']

        # Create first thread
        with concurrent.futures.ThreadPoolExecutor() as executor:
            while True:
                timer = executor.submit(self.start_trigger_timer, SHOOTING_TIME)
                if timer.result():
                    print("Take picture")
                    cord = self.gps.get_coordinates()
                    if self.cam.connect():
                        camera = executor.submit(self.cam.capture_photo_and_download)
                        pic_path = camera.result()
                        self.write_exif(pic_path, cord[0], cord[1], cord[2])
                        print(pic_path)

        # for pic in pictures_list:
        #     result = self.db.add_new_picture(PHOTOS_FOLDER + pic, coordinates["lat"], coordinates["lon"], coordinates["alt"], False, False)
        #     print(result)
        # not_uploaded_list = self.db.get_not_uploaded_lines()
        # print(not_uploaded_list)
        # set = self.db.set_picture_uploaded(not_uploaded_list[0]) # Send full row as list

    def start_trigger_timer(self, seconds):
        """
        Run in thread
        :return:
        """
        sleep(seconds)
        return True


if __name__ == "__main__":
    main = Main()
    main.run()
