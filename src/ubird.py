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
