import json

from etap3_images_dicts.dataclass_in_python import Furniture

fa = Furniture(25, 500, 500, 'aluminium')

fa_s = json.dumps(fa.__dict__)
# print(fa_s)  # zapis do string-u ==> json w stringu

with open('fa.json', 'w') as f:
    json.dump(fa.__dict__, f)   # zapis do pliku -- będzie zawierał json-a


ga_d = json.loads(fa_s)
ga = Furniture(**ga_d)

with open('fa.json', 'r') as f:
    za = json.load(f)   # dict na podstawie json-a z pliku
    print(za)
