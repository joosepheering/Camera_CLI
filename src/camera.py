import os
import signal
from subprocess import PIPE, Popen
from datetime import datetime
from time import sleep

GPHOTO_PROCESS_NAME = "gphoto2"
# SD_CARD_FOLDER = " "


def cmdline(command):
    process = Popen(
        args=command,
        stdout=PIPE,
        shell=True
    )
    return process.communicate()[0]


class Camera:

    def __init__(self, camera_name: str, folder_to_store: str):
        """
        Camera constructor.
        :param camera_name: Camera name when cam is connected and run 'gphoto2 --auto-detect'
        :param folder_to_store: Folder to save all the captured photos
        """
        self.camera_name = camera_name
        self.folder_to_store = folder_to_store

    def connect(self) -> bool:
        """
        Establish connection between camera and computer.
        :return: True if connected
        """
        # TODO Next line is ugly and unnecessary.
        connected = False
        while not connected:
            if self.__is_connected():
                print("Camera is connected")
                return True
            else:
                self.__kill_gphoto2_process()
                print("Camera not connected. Killing gphoto2 process.")

    def __is_connected(self) -> bool:
        """
        Check if camera is connected to main computer or not.
        :return: True if camera is connected
        """
        if self.camera_name in str(cmdline("gphoto2 --auto-detect")):
            return True
        else:
            return False

    def __kill_gphoto2_process(self):
        """
        When RPI starts, gphoto2 event is starting.
        # It needs to be killed before capturing photos, otherwise there is an error.
        # Kill > ps -A -> gvfs-gphoto2-vo
        :return: None
        """
        for line in cmdline("ps -A").splitlines():
            if GPHOTO_PROCESS_NAME in str(line):
                # Kill the process
                pid = int(line.split(None, 1)[0])
                os.kill(pid, signal.SIGKILL)

    def __get_new_image_name(self) -> str:
        """
        Create new and unique name for each image.
        :return: Full folder path of image + image name + file extension
        """
        return f"{self.folder_to_store}{datetime.now().strftime('%Y-%m-%d-%H:%M:%S')}.jpg"

    def __clear_camera_memory(self):
        """
        Clear memory in order to prevent infinite loop while capturing and downloading images.
        :return: None
        """
        # TODO Run gphoto2 --list-files when you have inserted memory card. If it causes trouble,
        #   create variable to store filepath name {} and uncomment next line
        # cmdline(f"gphoto2 --folder {SD_CARD_FOLDER} -R --delete-all-files")
        pass

    """
    def capture_photo(self):
        # TODO Capture error of not killed gphoto2 process
        self.__kill_gphoto2_process()
        cmdline("gphoto2 --trigger-capture")
    """

    def capture_photo_and_download(self) -> str:
        """
        Capture photo and save it to default folder.
        :return: image path of new photo
        """
        self.__kill_gphoto2_process()
        image_path = self.__get_new_image_name()
        cmdline(f"gphoto2 --capture-image-and-download --filename {image_path}")
        sleep(0.5)
        return image_path

