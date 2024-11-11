import os
import zipfile

# Pfad zu deinem spezifischen Ordner (bitte anpassen)
ordner_pfad = "C:\\Master\\GeoinfoPrj_Sem1\\Rohdaten\\alkis"  
# Sicherstellen, dass der Ordner existiert
if not os.path.exists(ordner_pfad):
    print("Der angegebene Ordner existiert nicht.")
    exit()

# Durchlaufe alle Dateien im Ordner
for datei in os.listdir(ordner_pfad):
    if datei.endswith(".zip"):
        zip_pfad = os.path.join(ordner_pfad, datei)
        try:
            # Entpacken in denselben Ordner
            with zipfile.ZipFile(zip_pfad, 'r') as zip_ref:
                zip_ref.extractall(ordner_pfad)
                print(f"{datei} wurde erfolgreich entpackt.")
        except zipfile.BadZipFile:
            print(f"Fehler: {datei} ist keine gültige ZIP-Datei.")

print("Entpacken abgeschlossen.")