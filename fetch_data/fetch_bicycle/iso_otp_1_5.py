import json
import re
import sys
import os
import requests
from pyproj import Transformer
from sqlalchemy import text
##########################################################################
project_dir = os.path.abspath(os.path.dirname(__file__))
project_root = os.path.abspath(os.path.join(project_dir, "..", ".."))

sys.path.append(project_root)
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

def fetch_otp_api(cor_dict,url, precision, cutoff, mode, speed, date, time):
    print ("gets here")
    # http://localhost:8080/otp/routers/current/isochrone?algorithm=accSampling&fromPlace=53.59860878,9.99349447&mode=BICYCLE&bikeSpeed=4.916667&date=2024-12-12&time=10:00:00&precisionMeters=10&cutoffSec=900
    results = {}
    error_results = {}
    total_tables = len(cor_dict)
    current_table_index = 0

    for table in cor_dict.keys():
        current_table_index += 1
        print_progress_bar(current_table_index, total_tables, prefix='Processing tables:', suffix='Complete', length=50)

        results[table] = []
        error_results[table] = []
        total_coords = len(cor_dict[table])
        current_coord_index = 0
        if "WALK" in mode:
            mode_speed = "walk"
        elif mode == "BICYCLE":
            mode_speed = "bike"
        else:
            mode = None
            print ("Check mode config because the speed param was set to None because it was not written WALK, TRANSIT or BICYCLE")

        for cor in cor_dict[table]:
            current_coord_index += 1
            print_progress_bar(current_coord_index, total_coords, prefix=f'Processing coordinates for table {table}:', suffix='Complete', length=50)
            request_url = f"{url}?algorithm=accSampling&fromPlace={cor[0][0]},{cor[0][1]}&mode={mode}&{mode_speed}Speed={speed}&date={date}&time={time}&precisionMeters={precision}&cutoffSec={cutoff}"
            #print (f"This is request url: {request_url}")
            try: 
                response = requests.get(request_url)
                response.raise_for_status() 
                response_data = response.json()
                results[table].append(response_data)
            except requests.exceptions.RequestException as e:
                print(f"Error fetching data for coordinates {cor} in table {table}: {e}")
                results[table].append(None) 
                error_results[table].append((cor, e))
    return results, error_results


# def fetch_otp_api(cor_dict, url, precision, cutoff, mode, speed, date, time):
#     """
#     API-Abfragefunktion, die auf die ersten 10 Features pro Tabelle begrenzt ist.

#     Parameters:
#     cor_dict (dict): Dictionary mit Tabellen als Keys und Listen von Koordinaten als Values.
#     url (str): Die API-URL.
#     precision (int): Genauigkeit in Metern.
#     cutoff (int): Maximale Zeit in Sekunden.
#     mode (str): Modus (WALK, BICYCLE, TRANSIT).
#     speed (float): Geschwindigkeit für den Modus.
#     date (str): Datum der Abfrage (YYYY-MM-DD).
#     time (str): Uhrzeit der Abfrage (HH:MM:SS).

#     Returns:
#     tuple: (results, error_results)
#     """
#     print("Starting limited API fetch...")

#     results = {}
#     error_results = {}
#     total_tables = len(cor_dict)
#     current_table_index = 0

#     for table in cor_dict.keys():
#         current_table_index += 1
#         print_progress_bar(current_table_index, total_tables, prefix='Processing tables:', suffix='Complete', length=50)

#         results[table] = []
#         error_results[table] = []

#         # Begrenzung auf die ersten 10 Features
#         total_coords = min(10, len(cor_dict[table]))
#         current_coord_index = 0

#         # Bestimme den Geschwindigkeitsparameter
#         if "WALK" in mode:
#             mode_speed = "walk"
#         elif mode == "BICYCLE":
#             mode_speed = "bike"
#         else:
#             mode = None
#             print("Check mode config because the speed param was set to None because it was not written WALK, TRANSIT or BICYCLE")

#         for cor in cor_dict[table][:total_coords]:  # **Slice bleibt hier erhalten**
#             current_coord_index += 1
#             print_progress_bar(current_coord_index, total_coords, prefix=f'Processing coordinates for table {table}:', suffix='Complete', length=50)

#             request_url = f"{url}?algorithm=accSampling&fromPlace={cor[0][0]},{cor[0][1]}&mode={mode}&{mode_speed}Speed={speed}&date={date}&time={time}&precisionMeters={precision}&cutoffSec={cutoff}"
            
#             try:
#                 response = requests.get(request_url)
#                 response.raise_for_status()
#                 response_data = response.json()
#                 results[table].append(response_data)

#                 # Debugging: Erfolgsmeldung
#                 print(f"✅ Successfully fetched data for {table} (coord {current_coord_index}/{total_coords})")

#             except requests.exceptions.RequestException as e:
#                 print(f"❌ Error fetching data for coordinates {cor} in table {table}: {e}")
#                 results[table].append(None)
#                 error_results[table].append((cor, e))

#     return results, error_results




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
            fetch_results, error_results = fetch_otp_api(cor_dict = cor_dict,url = url, precision = precision, cutoff= cutoff, mode = mode, speed = speed, date = date, time = time)

            for table, table_data in fetch_results.items():
                file_name = params["mode"].lower() + "_iso_" + str(params["speed"]).replace(".", "_") + "km_" + table.lower().replace(".", "_") + ".geojson"
                geojson_path = os.path.join(params["geojson_dir"], file_name)
                convert_json_2_geojson(json_data = table_data, filename = geojson_path)
                

            # geojson_folder_path = params["geojson_dir"]
            # data, config = create_config_copy_like_config_setup_dbjsonfile(data_format = [".geojson"], schema_name = params["new_isochrone_schema"], geojson_path = geojson_folder_path )
            # print (f"this is data: {data}")
            # print (f"this is config: {config}")
            # create_schema(data = data, db_con= db_con,suffix = "" )
            # table_names_and_paths_and_schema = create_table_name(data = data, config = config, suffix = "")
            # print (f"this is table_names_and_paths_and_schema: {table_names_and_paths_and_schema}")
            # upload2db(upload_config = table_names_and_paths_and_schema, db_con = db_con)
            # print (f"Uploaded {table} to database")
            
            print ("Get otp isos is finished!")
            conn.commit()
    except Exception as e:
        print(f"Error in get_otp_isos: {e}")
        conn.rollback()

def upload_fetched_isochrones_2_db(db_con, geojson_path, new_schema_name):
    geojson_folder_path = params["geojson_dir"]
    data, config = create_config_copy_like_config_setup_dbjsonfile(data_format = [".geojson"], schema_name = params["new_isochrone_schema"], geojson_path = geojson_folder_path )
    print (f"this is data: {data}")
    print (f"this is config: {config}")
    create_schema(data = data, db_con= db_con,suffix = "" )
    table_names_and_paths_and_schema = create_table_name(data = data, config = config, suffix = "")
    print (f"this is table_names_and_paths_and_schema: {table_names_and_paths_and_schema}")
    upload2db(upload_config = table_names_and_paths_and_schema, db_con = db_con)
    print ("uploading to database succesful")

            
############################################################################
# 1. Geojson wird nicht korrekt erstellt, die [] ganz am Anfang und Ende müssen weg
# 2. Es wird nur ein Polygon eingespeist und nicht alle von Hamburg
# 3. Ggf vorab nochmal gucken ob die fertigen Punktlayer auch wirklich alle nur im Raum Hamburg sind, sonst ist das ggf. ne Fehlerquelle
# 4. Import in die DB kann man von set up db nehmen, müsste genau das gleiche sein
################################################################################
with open ("C:\\Master\\GeoinfoPrj_Sem1\\Erreichbarkeitsanalyse\\fetch_data\\fetch_bicycle\\fetch_bicycle_config.json", "r") as file:
    config = json.load(file)
db_con = connect2DB()
geojson_path = config["fetch_otp"]["geojson_dir"]
new_schema_name = config["fetch_otp"]["new_isochrone_schema"]
for calc_set in config["fetch_otp"]["calculation_params"]:
    params = {
        "url": config["fetch_otp"]["server_url"],
        "new_isochrone_schema" : config["fetch_otp"]["new_isochrone_schema"],
        "schema" : config["fetch_otp"]["schema"],
        "geojson_dir": config["fetch_otp"]["geojson_dir"],
        "mode": list(calc_set["mode"].keys())[0],
        "speed": list(calc_set["mode"].values())[0],
        "date": calc_set["date"],
        "time": calc_set["time"],
        "precision": calc_set["precisionMeters"],
        "cutoff": calc_set["cutoffSec"]
    }

    get_otp_isos(db_con = db_con, params = params )
upload_fetched_isochrones_2_db(db_con = db_con, geojson_path = geojson_path, new_schema_name = new_schema_name)
# only walk
# http://localhost:8080/otp/routers/current/isochrone?algorithm=accSampling&fromPlace=53.59860878,9.99349447&mode=BICYCLE&bikeSpeed=4.916667&date=2024-12-12&time=10:00:00&precisionMeters=10&cutoffSec=900

# walk transit
# http://localhost:8080/otp/routers/current/isochrone?algorithm=accSampling&fromPlace=53.61542249,10.04778259&mode=WALK,TRANSIT&walkSpeed=1.34112&date=2024-12-12&time=10:00:00&precisionMeters=10&cutoffSec=900

# bicycle
# http://localhost:8080/otp/routers/current/isochrone?algorithm=accSampling&fromPlace=53.59860878,9.99349447&mode=BICYCLE&bikeSpeed=4.916667&date=2024-12-12&time=10:00:00&precisionMeters=10&cutoffSec=900

