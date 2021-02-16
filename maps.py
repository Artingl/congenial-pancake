import os
import requests


class Maps:
    def __init__(self):
        self.pos = [0, 0]
        self.spn = 0.002

    def getImage(self, c1, c2, layer, pt=None):
        res_path = "temp/tmp.png"
        if not os.path.isdir("temp"):
            os.mkdir("temp")

        map_request = f"http://static-maps.yandex.ru/1.x/?ll={float(c1) + self.pos[0]},{float(c2) + self.pos[1]}" \
                      f"&spn={self.spn},{self.spn}&l={layer}" + (f"&pt={pt[0]},{pt[1]}" if pt else "")
        response = requests.get(map_request)

        with open(res_path, "wb") as file:
            file.write(response.content)

        return res_path
