import json
import re
import sys
import os
import requests
from pyproj import Transformer
from sqlalchemy import text
##########################################################################
project_dir = os.path.abspath(os.path.dirname(__file__))
parent_dir = os.path.dirname(project_dir)
sys.path.append(parent_dir)
from data_processing_db_ops.intersect_with_buildings import get_tables
from data_processing_db_ops.util_fcts import connect2DB
from setup_db.geojson2localDB import create_schema, create_table_name, upload2db
#########################################################################
def extract_cors(schema, db_con):
    """
    Extract coordinates from features in tables of the given schema and return a dictionary.

    Args:
        schema (str): The database schema to extract tables from.
        db_con (object): The database connection object.

    Returns:
        dict: A dictionary with table names as keys and a list of coordinates as values.
    """
    try:
        tables_str_type = get_tables(schema, db_con) 
        result = {}
        for table in tables_str_type:
            result[table] = []
            # Query to fetch features (assuming a geometry column exists)
            query = text(f"""
            SELECT ST_AsText(geometry) as wkt_geometry
            FROM {schema}.{table}
            WHERE geometry IS NOT NULL;
            """)
            features = db_con.execute(query).fetchall()
            for feature in features:
                wkt_geometry = feature[0]
                if wkt_geometry:
                    # Parse WKT to extract coordinates (example for POINT/LINESTRING/POLYGON)
                    coordinates = extract_coordinates_from_wkt(wkt_geometry)
                    result[table].append(coordinates)

        return result

    except Exception as e:
        print(f"Error processing table {table}: {e}")
        return None

def transform_geometry_to_wgs84(coordinate):
    transformer = Transformer.from_crs(crs_from = "epsg:25832", crs_to = "epsg:4326")
    lon, lat = transformer.transform(coordinate[0], coordinate[1])
    return (lon, lat)
def extract_coordinates_from_wkt(wkt_geometry):
    """
    Parse WKT (Well-Known Text) geometry to extract coordinates.

    Args:
        wkt_geometry (str): The WKT geometry string.

    Returns:
        list: A list of coordinates extracted from the WKT geometry.
    """
    # Extract coordinate groups using a regular expression
    coordinate_pattern = re.compile(r"[-+]?[0-9]*\.?[0-9]+ [-+]?[0-9]*\.?[0-9]+")
    matches = coordinate_pattern.findall(wkt_geometry)
    # Convert matches to tuples of floats (coordinates)
    coordinates = [tuple(map(float, match.split())) for match in matches]
    wgs_coordinates = [transform_geometry_to_wgs84(coordinate) for coordinate in coordinates]
    return wgs_coordinates

def aggregate_feature_collections(json_data_list):
    """
    Aggregiert mehrere FeatureCollections zu einer einzigen.
    
    Args:
        json_data_list (list): Liste von GeoJSON-FeatureCollections.
    
    Returns:
        dict: Eine einzige GeoJSON-FeatureCollection mit aggregierten Features.
    """
    # Initialisiere die endgültige FeatureCollection
    aggregated_geojson = {
        "type": "FeatureCollection",
        "features": []
    }

    # Iteriere durch alle FeatureCollections und füge die Features hinzu
    for feature_collection in json_data_list:
        if isinstance(feature_collection, dict) and "features" in feature_collection:
            aggregated_geojson["features"].extend(feature_collection["features"])  # Features hinzufügen
    
    return aggregated_geojson
def convert_json_2_geojson(json_data, filename):
    """
    Aggregiert mehrere FeatureCollections und speichert sie als GeoJSON-Datei.
    
    Args:
        json_data_list (list): Liste von GeoJSON-FeatureCollections.
        filename (str): Der Name der Ausgabedatei.
    """
    # Aggregiere die Features
    aggregated_geojson = aggregate_feature_collections(json_data)
    
    # GeoJSON in Datei speichern
    with open(filename, "w") as file:
        json.dump(aggregated_geojson, file)
    
    print(f"GeoJSON-Datei '{filename}' wurde erstellt.")


def print_progress_bar(iteration, total, prefix='', suffix='', length=50, fill='█'):
    """
    Erstellt eine Fortschrittsanzeige im Terminal.

    Args:
        iteration (int): Der aktuelle Fortschritt (z. B. die aktuelle Iteration).
        total (int): Die Gesamtanzahl der Iterationen.
        prefix (str): Text vor der Fortschrittsanzeige.
        suffix (str): Text nach der Fortschrittsanzeige.
        length (int): Die Länge der Fortschrittsanzeige in Zeichen.
        fill (str): Das Zeichen, das für den Fortschritt verwendet wird.
    """
    percent = ("{0:.1f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    sys.stdout.write(f'\r{prefix} |{bar}| {percent}% {suffix}')
    sys.stdout.flush()
    if iteration == total:
        print()

# def fetch_otp_api(cor_dict,url, precision, cutoff, mode, speed, date, time):
#     print ("gets here")
#     # http://localhost:8080/otp/routers/current/isochrone?algorithm=accSampling&fromPlace=53.59860878,9.99349447&mode=BICYCLE&bikeSpeed=4.916667&date=2024-12-12&time=10:00:00&precisionMeters=10&cutoffSec=900
#     results = {}
#     error_results = {}
#     total_tables = len(cor_dict)
#     current_table_index = 0

#     for table in cor_dict.keys():
#         current_table_index += 1
#         print_progress_bar(current_table_index, total_tables, prefix='Processing tables:', suffix='Complete', length=50)

#         results[table] = []
#         error_results[table] = []
#         total_coords = len(cor_dict[table])
#         current_coord_index = 0

#         for cor in cor_dict[table]:
#             current_coord_index += 1
#             print_progress_bar(current_coord_index, total_coords, prefix=f'Processing coordinates for table {table}:', suffix='Complete', length=50)
#             request_url = f"{url}?algorithm=accSampling&fromPlace={cor[0][0]},{cor[0][1]}&mode={mode}&bikeSpeed={speed}&date={date}&time={time}&precisionMeters={precision}&cutoffSec={cutoff}"
#             try: 
#                 response = requests.get(request_url)
#                 response.raise_for_status() 
#                 response_data = response.json()
#                 results[table].append(response_data)
#             except requests.exceptions.RequestException as e:
#                 print(f"Error fetching data for coordinates {cor} in table {table}: {e}")
#                 results[table].append(None) 
#                 error_results[table].append((cor, e))
#     return results, error_results


def fetch_otp_api(cor_dict, url, precision, cutoff, mode, speed, date, time):
    print("gets here")
    # http://localhost:8080/otp/routers/current/isochrone?algorithm=accSampling&fromPlace=53.59860878,9.99349447&mode=BICYCLE&bikeSpeed=4.916667&date=2024-12-12&time=10:00:00&precisionMeters=10&cutoffSec=900
    results = {}
    error_results = {}

    # Nur die erste Tabelle aus cor_dict für das Testen auswählen
    if cor_dict:
        first_table = next(iter(cor_dict.keys()))
        print(f"Processing only the first table: {first_table}")

        results[first_table] = []
        error_results[first_table] = []

        # Alle Features der ersten Tabelle abfragen
        total_coords = len(cor_dict[first_table])
        current_coord_index = 0

        for cor in cor_dict[first_table]:
            current_coord_index += 1
            print_progress_bar(current_coord_index, total_coords, prefix=f'Processing coordinates for table {first_table}:', suffix='Complete', length=50)
            request_url = f"{url}?algorithm=accSampling&fromPlace={cor[0][0]},{cor[0][1]}&mode={mode}&bikeSpeed={speed}&date={date}&time={time}&precisionMeters={precision}&cutoffSec={cutoff}"
            print (f"this is the request url: {request_url}")
            try:
                response = requests.get(request_url)
                response.raise_for_status()
                response_data = response.json()
                results[first_table].append(response_data)
            except requests.exceptions.RequestException as e:
                print(f"Error fetching data for coordinates {cor} in table {first_table}: {e}")
                results[first_table].append(None)
                error_results[first_table].append((cor, e))

    return results, error_results

def clean_geojson_file(filename):
    with open(filename, "r") as file:
        content = file.read()  # Die gesamte Datei als String lesen

    # Die eckigen Klammern entfernen
    if content.startswith("[") and content.endswith("]"):
        content = content[1:-1].strip()  # Erstes und letztes Zeichen entfernen

    # Den bereinigten Inhalt wieder in die Datei schreiben
    with open(filename, "w") as file:
        file.write(content)

    print(f"Bereinigte GeoJSON-Datei '{filename}'.")
def create_config_copy_like_config_setup_dbjsonfile(data_format, schema_name, geojson_path):
    print (f"this is the geojson path in create config copy: {geojson_path}")
    # this is the original config format: 
# {
#   "geojson2localdb": {
#     "config": {
#       "data_format": [".json", ".geojson"]
#     },
#     "data": {
#       "ausserschulangebote": "C:\\Master\\GeoinfoPrj_Sem1\\Rohdaten\\indikatoren_kids\\ausserschuleBetreuungBildung",
# this function transforms the generated data so that i can be passed into the already existing function
    config = {
        "data_format": data_format,
    }
    data = {
        schema_name : geojson_path
    }
    return data, config

def get_otp_isos(db_con, params):
    url = params["url"]
    mode = params["mode"]
    speed = params["speed"]
    date = params["date"]
    time = params["time"]
    precision = params["precision"]
    cutoff = params["cutoff"]
    try:
        with db_con.connect() as conn:
            cor_dict = extract_cors(db_con=conn, schema = params["schema"])
            print ("1")
            fetch_results, error_results = fetch_otp_api(cor_dict = cor_dict,url = url, precision = precision, cutoff= cutoff, mode = mode, speed = speed, date = date, time = time)
            print ("2")

            for table, table_data in fetch_results.items():
                print ("3")
                file_name = "otp_iso_" + table + ".geojson"
                geojson_path = os.path.join(params["geojson_dir"], file_name)
                geojson_folder_path = params["geojson_dir"]
                convert_json_2_geojson(json_data = table_data, filename = geojson_path)
                
                print (f"this is the geojson path: {geojson_path}")
                #clean_geojson_file(filename = geojson_path)
                data, config = create_config_copy_like_config_setup_dbjsonfile(data_format = [".geojson"], schema_name = params["new_isochrone_schema"], geojson_path = geojson_folder_path )
                print (f"this is data: {data}")
                print (f"this is config: {config}")
                create_schema(data = data, db_con= db_con,suffix = "" )
                table_names_and_paths_and_schema = create_table_name(data = data, config = config, suffix = "")
                print (f"this is table_names_and_paths_and_schema: {table_names_and_paths_and_schema}")
                upload2db(upload_config = table_names_and_paths_and_schema, db_con = db_con)
                print (f"Uploaded {table} to database")
            
            print ("Get otp isos is finished!")
            conn.commit()

            
    except Exception as e:

        print(f"Error: {e}")
        conn.rollback()


############################################################################
# 1. Geojson wird nicht korrekt erstellt, die [] ganz am Anfang und Ende müssen weg
# 2. Es wird nur ein Polygon eingespeist und nicht alle von Hamburg
# 3. Ggf vorab nochmal gucken ob die fertigen Punktlayer auch wirklich alle nur im Raum Hamburg sind, sonst ist das ggf. ne Fehlerquelle
# 4. Import in die DB kann man von set up db nehmen, müsste genau das gleiche sein
################################################################################
with open ("C:\\Master\\GeoinfoPrj_Sem1\\Erreichbarkeitsanalyse\\fetch_data\\fetch_data_config.json", "r") as file:
    config = json.load(file)
params = {
    "url": config["fetch_otp"]["server_url"],
    "new_isochrone_schema" : config["fetch_otp"]["new_isochrone_schema"],
    "schema" : config["fetch_otp"]["schema"],
    "geojson_dir": config["fetch_otp"]["geojson_dir"],
    "mode": list(config["fetch_otp"]["calculation_params"]["mode"].keys())[0],
    "speed": list(config["fetch_otp"]["calculation_params"]["mode"].values())[0],
    "date": config["fetch_otp"]["calculation_params"]["date"],
    "time": config["fetch_otp"]["calculation_params"]["time"],
    "precision": config["fetch_otp"]["calculation_params"]["precisionMeters"],
    "cutoff": config["fetch_otp"]["calculation_params"]["cutoffSec"]
}
db_con = connect2DB()
get_otp_isos(db_con = db_con, params = params )
# only walk
# http://localhost:8080/otp/routers/current/isochrone?algorithm=accSampling&fromPlace=53.59860878,9.99349447&mode=BICYCLE&bikeSpeed=4.916667&date=2024-12-12&time=10:00:00&precisionMeters=10&cutoffSec=900

# walk transit
# http://localhost:8080/otp/routers/current/isochrone?algorithm=accSampling&fromPlace=53.61542249,10.04778259&mode=WALK,TRANSIT&walkSpeed=1.34112&date=2024-12-12&time=10:00:00&precisionMeters=10&cutoffSec=900

# bicycle
# http://localhost:8080/otp/routers/current/isochrone?algorithm=accSampling&fromPlace=53.59860878,9.99349447&mode=BICYCLE&bikeSpeed=4.916667&date=2024-12-12&time=10:00:00&precisionMeters=10&cutoffSec=900

