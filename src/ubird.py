"""
uBird handler.

It:

"""
import os
from subprocess import PIPE, Popen

TOKEN = ""


def cmdline(command):
    process = Popen(
        args=command,
        stdout=PIPE,
        shell=True
    )
    return process.communicate()[0]


class UBird:

    def __init__(self, project_id: str):
        self.project_id = project_id
        pass

    def authenticate(self, username: str, password: str) -> bool:
        """

        :param username:
        :param password:
        :return: True if success
        """
        pass

    def photo_is_uploaded(self, photo_path: str) -> bool:
        """
        Make request to ubird to verify, if this photo has been uploaded to ubird. Use checksum.
        :param photo_path: photo
        :return: True if it is uploaded.
        """
        pass

    def upload_photo(self, photo_path: str):
        """
        1. Check if photo exists, both in json file and in folder
        2. Get Checksum from uBird.
            IF TRUE (already uploaded):
                change json "uploaded" == True
            ELSE:
                upload photo to ubird
                IF return == 200:
                    change json "uploaded" == True
                    return True
                ELSE:
                    change json "uploaded" == False
                    return False

        :param photo_path:
        :return:
        """
        # TODO Return result
        # TODO If true, then change json file "uploaded" => True
        return cmdline(f'curl -X POST "https://api.ubird.wtf/ubird/upload/project/{self.project_id}/pictures" -H "accept: */*" -H "Content-Type: multipart/form-data" -H "Authorization: Bearer {TOKEN}" -F "file=@{photo_path};type=image/jpeg"')

    def import_photo(self) -> bool:
        """
        1. Check if photo exists
        2. Import photo to ubird
            IF return == 200:
                change json "imported" == True
                return True
            ELSE:
                change json "imported" == False
                return False
        :param photo_path:
        :param lat:
        :param lon:
        :param line_id:
        :return: True if is imported
        """
        powerline_name = "Demo"
        lat1 = 89.9
        lon1 = -179.9
        lat2 = -89.9
        lon2 = 179.9

        return cmdline(f'curl -X POST "https://api.ubird.wtf/ubird/jobs/project/{self.project_id}/uploads/{lat1}/{lon1}/{lat2}/{lon2}/start?powerLineName={powerline_name}" -H "accept: application/json" -H "Authorization: Bearer {TOKEN}"')

    def __photo_exist(self, photo_path):
        """

        :param photo_path: path to check
        :return: True if exists
        """

