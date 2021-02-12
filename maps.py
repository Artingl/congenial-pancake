import os

import requests


class Maps:
    def __init__(self):
        pass

    def getImage(self, c1, c2):
        res_path = "temp/tmp.png"
        if not os.path.isdir("temp"):
            os.mkdir("temp")

        map_request = f"http://static-maps.yandex.ru/1.x/?ll={c1},{c2}8&spn=0.002,0.002&l=map"
        response = requests.get(map_request)

        with open(res_path, "wb") as file:
            file.write(response.content)

        return res_path
