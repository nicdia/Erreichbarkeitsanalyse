import os
import zipfile


ordner_pfad = "C:\\Master\\GeoinfoPrj_Sem1\\Rohdaten\\alkis"

if not os.path.exists(ordner_pfad):
    print("Der angegebene Ordner existiert nicht.")
    exit()

for datei in os.listdir(ordner_pfad):
    if datei.endswith("json"):
        new_name = datei.replace("app_", "").replace("_EPSG_25832", "")
        old_path = os.path.join(ordner_pfad, datei)
        new_path = os.path.join(ordner_pfad, new_name)
        os.rename(old_path, new_path)


print("Entpacken abgeschlossen.")