import json
import os
import piexif
from PIL import Image
from subprocess import PIPE, Popen


def cmdline(command):
    process = Popen(
        args=command,
        stdout=PIPE,
        shell=True
    )
    return process.communicate()[0]


class DB:
    """
    FLOW
    1. picture has been created to folder.
    2.
    """

    def __init__(self, json_file: str):
        """
        Keeps track of:
        picture paths,
        checksum,
        coordinates,
        uploaded to ubird,
        imported to ubird
        :param json_file: json file to store pictures data
        """
        self.json_file = json_file

    def add_new_picture(self, path: str, lat: float, lon: float, alt: float, uploaded: bool, imported: bool) -> bool:
        """
        Check if file already exists with checksum.
        If not, then add new JSON item to file.

        :param path:
        :param checksum:
        :param lat:
        :param lon:
        :param alt:
        :param uploaded:
        :param imported
        :return: True if file has been added
        """
        # Check if file exists.
        if self.__picture_exists(path):
            #  Write lat/lon to exif
            if self.__write_exif(path, lat, lon, alt):
                # Create MD5 Checksum
                checksum = self.__generate_checksum(path)
                # Create JSON
                data = {'picture': []}
                data['picture'].append({
                    'path': path,
                    'checksum': checksum,
                    'lat': lat,
                    'lon': lon,
                    'alt': alt,
                    'uploaded': uploaded,
                    'imported': imported
                })
                try:
                    if not os.path.exists(self.json_file):
                        open(self.json_file, 'w+').close()
                    # Clear file and write coordinates
                    with open(self.json_file, 'a+') as json_file:
                        json.dump(data, json_file)
                    json_file.close()
                    return True
                except IOError as e:
                    print(f"Something went wrong when writing to the file: {e}")
                    return False

    def get_not_uploaded_lines(self) -> list:
        """

        :return: list of JSON items of pictures that are not uploaded
        """
        pass

    def get_not_imported_lines(self) -> list:
        """

        :return: list of JSON items of pictures that are not imported
        """
        pass

    def __picture_exists(self, picture_path: str) -> bool:
        return os.path.isfile(picture_path)

    def __write_exif(self, picture_path: str, lat: float, lon: float, alt: float):
        """

        :param picture_path:
        :param lat:
        :param lon:
        :return:
        """
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

    def __generate_checksum(self, picture_path) -> str:
        """
        Create MD5 checksum.

        :param picture_path: picture to use
        :return: checksum
        """
        md5 = str(cmdline(f"md5 {picture_path}"))
        return str(md5.split('= ')[1])[:-3]

"""
1. Generate JSON file. 
    IF photos is empty:
        create empty json file
    ELSE: 
        loop through all images in this file
            get_path
            get_coordinate_from_exif
            generate_checksum
            write_to_json_file






"""