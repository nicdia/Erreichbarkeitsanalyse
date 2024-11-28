import os
import requests
import json
from dotenv import load_dotenv
import time

# .env-Datei laden
load_dotenv()

# API-Schlüssel aus der .env-Datei laden
API_KEY = os.getenv("GMAPS_API_KEY")
if not API_KEY:
    raise ValueError("API-Schlüssel nicht in der .env-Datei gefunden. Bitte prüfen!")

# Basis-URL für die Places API
BASE_URL = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"

# Typen, die abgerufen werden sollen
search_types = [
    {"type": "playground", "filename": "spielplaetze_hamburg.geojson"},
    {"type": "park", "filename": "parks_hamburg.geojson"},
    {"type": "dentist", "filename": "kinderzahnaerzte_hamburg.geojson", "keyword": "children"}
]

# Funktion zum Abrufen und Speichern von GeoJSON mit Paging und Debugging
def fetch_places_with_paging(search_type, filename, keyword=None):
    params = {
        "location": "53.5511,9.9937",  # Hamburg Zentrum
        "radius": 15000,               # Radius in Metern
        "type": search_type,           # Ortstyp
        "key": API_KEY
    }
    if keyword:
        params["keyword"] = keyword  # Keyword hinzufügen (z.B. "children" für Kinderzahnärzte)

    all_results = []  # Gesamte Ergebnisse sammeln
    page = 1  # Für Debugging: Seite der Anfrage

    while True:
        print(f"[DEBUG] Sende Anfrage für Seite {page} mit Typ: {search_type}")
        response = requests.get(BASE_URL, params=params)

        if response.status_code == 200:
            data = response.json()
            
            # Debug: API-Antwort anzeigen
            print(f"[DEBUG] Antwort von Seite {page}:")
            print(json.dumps(data, indent=4, ensure_ascii=False))
            
            # Ergebnisse hinzufügen
            results = data.get("results", [])
            if not results:
                print(f"[DEBUG] Keine Ergebnisse für Seite {page}")
                break

            all_results.extend(results)
            print(f"[DEBUG] Anzahl der Ergebnisse auf Seite {page}: {len(results)}")
            
            # Prüfen, ob weitere Seiten existieren
            next_page_token = data.get("next_page_token")
            if next_page_token:
                print(f"[DEBUG] Nächste Seite gefunden, warte 2 Sekunden...")
                params["pagetoken"] = next_page_token
                time.sleep(2)  # Google empfiehlt, 2 Sekunden zu warten
                page += 1
            else:
                print("[DEBUG] Keine weiteren Seiten verfügbar")
                break
        else:
            print(f"[ERROR] Fehler bei der API-Anfrage (Statuscode: {response.status_code})")
            print(response.text)
            break

    # Debug: Gesamtanzahl der abgerufenen Ergebnisse
    print(f"[DEBUG] Gesamte Anzahl der abgerufenen Ergebnisse für {search_type}: {len(all_results)}")

    # GeoJSON erstellen
    geojson_data = {
        "type": "FeatureCollection",
        "features": []
    }
    for place in all_results:
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [
                    place["geometry"]["location"]["lng"],  # Longitude
                    place["geometry"]["location"]["lat"]   # Latitude
                ]
            },
            "properties": {
                "name": place["name"],
                "address": place.get("vicinity"),        # Adresse
                "types": place.get("types", [])          # Typen
            }
        }
        geojson_data["features"].append(feature)

    # GeoJSON speichern
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(geojson_data, file, ensure_ascii=False, indent=4)
    print(f"[DEBUG] GeoJSON erfolgreich gespeichert: {filename}")

# Hauptprozess: Alle Typen abrufen und speichern
for search in search_types:
    fetch_places_with_paging(search["type"], search["filename"], search.get("keyword"))