import os
import requests


class Maps:
    def __init__(self):
        self.pos = [0, 0]
        self.spn = 0.002
        self.pt = {}
        self.show_pt = True

    def getAddress(self, c1, c2):
        url = f"https://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b" \
              f"&geocode={c1},{c2}&format=json"
        response = requests.get(url).json()
        toponym = response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        toponym_address = toponym["metaDataProperty"]["GeocoderMetaData"]["text"]
        postal = "Not found!"
        try:
            postal = response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["metaDataProperty"][
                "GeocoderMetaData"]["Address"]["postal_code"]
        except Exception:
            pass

        return toponym_address + f", Postal code: {postal}"

    def getImage(self, parent_class, c1=0, c2=0, geo=0, layer=''):
        res_path = "temp/tmp.png"
        if not os.path.isdir("temp"):
            os.mkdir("temp")

        pt = ""
        if self.show_pt:
            pt = '&pt='
            for i in self.pt.items():
                pt += f'{i[1][0]},{i[1][1]},pmwtm{i[0]}~'
            pt = pt[:-1]

        if c1 != 0 and c2 != 0:
            if (c1, c2) not in self.pt.values():
                self.pt[1] = (c1, c2)
                return self.getImage(parent_class, c1, c2, geo, layer)
            map_request = f"http://static-maps.yandex.ru/1.x/?ll={float(c1) + self.pos[0]},{float(c2) + self.pos[1]}" \
                          f"&spn={self.spn},{self.spn}&l={layer}" + pt
        if geo != 0:
            geo = '+'.join(geo.split())
            geocoder = f'https://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode={geo}&format=json'
            response = requests.get(geocoder)
            geocoder = response.json()
            toponym = geocoder["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
            toponym_coodrinates = toponym["Point"]["pos"]
            splitted = toponym_coodrinates.split()
            x = splitted[0]
            y = splitted[1]
            if (x, y) not in self.pt.values():
                self.pt[1] = (x, y)
            return self.getImage(parent_class, x, y, 0, layer)
        response = requests.get(map_request)
        parent_class.adress_label.setText("Info: " + self.getAddress(c1, c2))

        with open(res_path, "wb") as file:
            file.write(response.content)

        return res_path
