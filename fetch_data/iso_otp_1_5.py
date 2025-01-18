import os
import requests
import geopandas as gpd
from shapely.geometry import Point, MultiPoint
from datetime import datetime

# OTP 1.5.0 API-Endpunkt
OTP_SERVER_URL = "http://localhost:8080/otp/routers/current/isochrone"

# Parameter für die Berechnung
MODES = "WALK,TRANSIT"  # Transportmodi
ARRIVE_BY = "TRUE"  # Ankunft statt Abfahrt
MAX_WALK_DISTANCE = 99000  # Maximale Fußwegdistanz in Metern
WALK_RELUCTANCE = 5  # Fußweg-Nachgiebigkeit (höhere Werte bedeuten ungern zu Fuß gehen)
MIN_TRANSFER_TIME = 600  # Minimale Umstiegszeit in Sekunden
CUTOFFS = [900]  # Zeitgrenzen in Sekunden

# Eingabe: GeoJSON-Datei
GEOJSON_FILE = "de_hh_up_hochschulen.geojson"

# GeoJSON-Daten laden
points_gdf = gpd.read_file(GEOJSON_FILE)

# Koordinatensystem in EPSG:4326 transformieren (falls nicht vorhanden)
if points_gdf.crs != "EPSG:4326":
    points_gdf = points_gdf.to_crs(epsg=4326)

# Ergebnisse speichern
isochrone_features = []  # Liste für alle Isochronen-Features

# Isochronen für jeden Punkt berechnen
for idx, point in points_gdf.iterrows():
    geometry = point.geometry

    # Nur mit Point- oder MultiPoint-Geometrien arbeiten
    if isinstance(geometry, Point):
        lon, lat = geometry.x, geometry.y
    elif isinstance(geometry, MultiPoint):
        if len(geometry.geoms) > 0:
            first_point = geometry.geoms[0]
            lon, lat = first_point.x, first_point.y
        else:
            print(f"MultiPoint bei Punkt {idx} enthält keine Geometrien. Übersprungen.")
            continue
    else:
        print(f"Geometrie-Typ {type(geometry)} bei Punkt {idx} wird übersprungen.")
        continue

    # Datum und Zeit generieren
    iso_date = datetime(2024,12,12).strftime("%m-%d-%Y")
    #iso_date = datetime.now().strftime("%m-%d-%Y")  # Format: MM-DD-YYYY
    iso_time = datetime.now().strftime("%I:%M%p").lower()  # Format: HH:MMam/pm

    # Anfrage-Parameter zusammenstellen
    params = {
        "toPlace": f"{lat},{lon}",
        "fromPlace": f"{lat},{lon}",
        "arriveBy": ARRIVE_BY,
        "mode": MODES,
        "date": iso_date,
        "time": iso_time,
        "maxWalkDistance": MAX_WALK_DISTANCE,
        "walkReluctance": WALK_RELUCTANCE,
        "minTransferTime": MIN_TRANSFER_TIME
        #"precisionMeters": 10
    }

    # CUTOFFS hinzufügen
    for cutoff in CUTOFFS:
        params[f"cutoffSec"] = cutoff

    # Anfrage an den OTP-Server senden
    try:
        response = requests.get(OTP_SERVER_URL, params=params)
        response.raise_for_status()  # Prüfen auf HTTP-Fehler

        # Antwort als GeoJSON laden
        isochrone_geojson = response.json()

        # Feature-Collection erweitern
        for feature in isochrone_geojson.get("features", []):
            feature["properties"].update({"point_index": idx, "latitude": lat, "longitude": lon})
            isochrone_features.append(feature)

        print(f"Isochrone für Punkt {idx} erfolgreich verarbeitet.")

    except requests.RequestException as e:
        print(f"Fehler bei der Anfrage für Punkt {idx}: {e}")

# Alle Isochronen in einer Datei speichern
output_file = "all_isochrones_neu.geojson"
output_geojson = {
    "type": "FeatureCollection",
    "features": isochrone_features,
}

with open(output_file, "w", encoding="utf-8") as f:
    import json
    json.dump(output_geojson, f, ensure_ascii=False, indent=2)

print(f"Alle Isochronen wurden in '{output_file}' gespeichert.")
