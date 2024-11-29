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

# Basis-URL für die Nearby Search API
BASE_URL = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"

# Liste der zentralen Punkte in Hamburg, um die Stadt abzudecken
locations = [
    "53.5511,9.9937",  # Hamburg Zentrum
    "53.5848,10.0057",  # Nordöstlich
    "53.5286,9.9861",  # Südlich
    "53.5522,10.0230",  # Östlich
    "53.5570,9.9410",  # Westlich
]

# Erweiterter Code für Nearby Search
def fetch_places_multiple_locations(search_type, filename, keyword=None):
    all_results = []
    for location in locations:
        params = {
            "location": location,
            "radius": 50000,  # Maximaler Radius
            "type": search_type,
            "key": API_KEY
        }
        if keyword:
            params["keyword"] = keyword

        # Abrufen der Daten für jeden Standort
        print(f"[DEBUG] Sende Anfrage für Standort {location} mit Typ: {search_type}")
        response = requests.get(BASE_URL, params=params)
        if response.status_code == 200:
            data = response.json()
            results = data.get("results", [])
            all_results.extend(results)

            # Prüfen, ob es weitere Seiten gibt
            next_page_token = data.get("next_page_token")
            while next_page_token:
                print(f"[DEBUG] Nächste Seite gefunden, warte 2 Sekunden...")
                time.sleep(2)  # Google empfiehlt, 2 Sekunden zu warten
                params["pagetoken"] = next_page_token
                response = requests.get(BASE_URL, params=params)
                if response.status_code == 200:
                    data = response.json()
                    results = data.get("results", [])
                    all_results.extend(results)
                    next_page_token = data.get("next_page_token")
                else:
                    print(f"[ERROR] Fehler bei der API-Anfrage (Statuscode: {response.status_code})")
                    break
        else:
            print(f"[ERROR] Fehler bei der API-Anfrage (Statuscode: {response.status_code})")
            print(response.text)

    # Duplikate entfernen basierend auf Place ID
    unique_places = {place["place_id"]: place for place in all_results}
    all_results = list(unique_places.values())

    # GeoJSON erstellen und speichern
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
                "address": place.get("vicinity"),
                "types": place.get("types", []),
                "rating": place.get("rating"),  # Bewertung
                "user_ratings_total": place.get("user_ratings_total")  # Anzahl der Bewertungen
            }
        }
        geojson_data["features"].append(feature)

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(geojson_data, file, ensure_ascii=False, indent=4)
    print(f"[DEBUG] GeoJSON erfolgreich gespeichert: {filename}")

# Beispielaufruf
fetch_places_multiple_locations("playground", "spielplaetze_hamburg.geojson")
fetch_places_multiple_locations("park", "parks_hamburg.geojson")