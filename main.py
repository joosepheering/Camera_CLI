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

CAMERA_NAME = "Sony Alpha-A6000"
PHOTOS_FOLDER = "/Users/roos/Desktop/Pictures/"
JSON_FILE = "/Users/roos/Desktop/gphoto_json/db.json"


class Main:

    def __init__(self):
        self.gps = GPS()
        self.db = DB(JSON_FILE)
        self.cam = Camera(CAMERA_NAME, PHOTOS_FOLDER)
        # self.ubird = UBird
        # self.ubird.authenticate()

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
        coordinates = self.gps.get_coordinates()
        pictures_list = ['DSC00325.JPG', 'DSC00324.JPG']
        for pic in pictures_list:
            result = self.db.add_new_picture(PHOTOS_FOLDER + pic, coordinates["lat"], coordinates["lon"], coordinates["alt"], False, False)
            print(result)

    def start_trigger_timer(self):
        """
        Run in thread
        :return:
        """
        pass


if __name__ == "__main__":
    main = Main()
    main.run()
