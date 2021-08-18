import csv
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

    def __init__(self, csv_file: str):
        """
        Keeps track of:
        picture paths,
        checksum,
        coordinates,
        uploaded to ubird,
        imported to ubird
        :param csv_file: json file to store pictures data
        """
        self.csv_file = csv_file
        self.create_csv_file()

    def create_csv_file(self):
        try:
            if not os.path.exists(self.csv_file):
                with open(self.csv_file, 'w+') as csv_file:
                    reader = csv.DictReader(csv_file)
                    for row in reader:
                        print(row)
                csv_file.close()
                return True
        except IOError as e:
            print(f"Something went wrong when writing to the file: {e}")
            return False

    def add_new_picture(self, path: str, lat: float, lon: float, alt: float, uploaded: bool, imported: bool) -> bool:

        # Check if file exists.
        if self.__picture_exists(path):
            #  Write lat/lon to exif
            if self.__write_exif(path, lat, lon, alt):
                # Create MD5 Checksum
                checksum = self.__generate_checksum(path)
                # Create CSV
                fields = [path, checksum, lat, lon, alt, uploaded, imported]
                try:
                    with open(self.csv_file, 'a') as f:
                        writer = csv.writer(f)
                        writer.writerow(fields)
                        f.close()
                    return True
                except IOError as e:
                    print(f"Something went wrong when writing to the file: {e}")
                    return False

    def get_not_uploaded_lines(self) -> list:
        try:
            rows_list = []
            with open(self.csv_file, 'r') as f:
                reader = csv.reader(f)
                for row in reader:
                    if row[5] == "False":
                        rows_list.append(row)
                f.close()
            return rows_list
        except IOError as e:
            print(f"Something went wrong when writing to the file: {e}")

    def get_not_imported_lines(self) -> list:
        try:
            rows_list = []
            with open(self.csv_file, 'r') as f:
                reader = csv.reader(f)
                for row in reader:
                    if row[6] == "False":
                        rows_list.append(row)
                f.close()
            return rows_list
        except IOError as e:
            print(f"Something went wrong when writing to the file: {e}")
            return []

    def set_picture_uploaded(self, row_to_change):
        try:
            csv_list = []
            pointer = None
            with open(self.csv_file, 'r') as f:
                reader = csv.reader(f)
                i = 0
                for row in reader:
                    if row[1] == row_to_change[1]:
                        pointer = i
                    else:
                        csv_list.append(row)
                    i += 1
                f.close()

            with open(self.csv_file, 'a') as f:
                writer = csv.writer(f)
                f.close()




        except IOError as e:
            print(f"Something went wrong when writing to the file: {e}")
            return []

    def __picture_exists(self, picture_path: str) -> bool:
        return os.path.isfile(picture_path)

    def __write_exif(self, picture_path: str, lat: float, lon: float, alt: float):

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

        md5 = str(cmdline(f"md5 {picture_path}"))
        return str(md5.split('= ')[1])[:-3]
