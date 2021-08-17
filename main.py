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
from src.camera import Camera

CAMERA_NAME = "Sony Alpha-A6000"
PHOTOS_FOLDER = "/home/roos/Desktop/gphoto/"


class Main:

    def __init__(self):
        cam = Camera(CAMERA_NAME, PHOTOS_FOLDER)
        cam.connect()
        photo = cam.capture_photo_and_download()
        print(photo)


if __name__ == "__main__":
    main = Main()
