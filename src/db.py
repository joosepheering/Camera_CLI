import json
import os


class DB:

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

    def open_file(self, path) -> object:
        """

        :param path: JSON file path
        :return: file
        """
        pass

    def add_new_picture(self, path: str, checksum: str, lat: str, lon: str, uploaded: bool, imported: bool) -> bool:
        """
        Check if file already exists with checksum.
        If not, then add new JSON item to file.

        :param path:
        :param checksum:
        :param lat:
        :param lon:
        :param uploaded:
        :param imported
        :return: True if file has been added
        """
        # TODO Check if file exists.
        data = {'picture': []}
        data['picture'].append({
            'path': path,
            'checksum': checksum,
            'lat': lat,
            'lon': lon,
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
        except IOError as e:
            print(f"Something went wrong when writing to the file: {e}")

    def get_not_uploaded_lines(self) -> list:
        """

        :return: list of JSON items of pictures that are not uploaded
        """

    def get_not_imported_lines(self) -> list:
        """

        :return: list of JSON items of pictures that are not imported
        """

    def write_exif(self,checksum: str, lat: str, lon: str):


    def __get_coordinates_from_exif(self, picture_path) -> dict:
        """
        Read picture exif and extract coordinates. Needed in case new, already geo tagged picture is added to folder,
        that is not is JSON file.

        :param picture_path: pictre to use
        :return: {"lat": 43.3243, "lon": 21.4213}
        """

    def __generate_checksum(self, picture_path) -> str:
        """
        Create MD5 checksum.

        :param picture_path: picture to use
        :return: checksum
        """


    def __generate_json_file(self, file_path: str, pictures_folder: str) -> bool:
        """

        :param file_path: JSON file path to generate
        :param pictures_folder: Pictures folder to use
        :return: True, when generated
        """



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