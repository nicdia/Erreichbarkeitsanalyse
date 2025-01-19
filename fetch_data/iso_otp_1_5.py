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
processing_dir = os.path.join(parent_dir,"data_processing_db_ops")
sys.path.append(parent_dir)
from data_processing_db_ops.intersect_with_buildings import get_tables
from data_processing_db_ops.util_fcts import connect2DB
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
                    result[table] = coordinates
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

def convert_json_2_geojson(json_data, precision, cutoff, mode, speed, date, time, filename):
    if not isinstance(json_data, dict) or not json_data:
        raise ValueError("Input JSON data must be a non-empty dictionary.")

    
    for features in json_data.values():
        print (f"this is features: {features}")
        with open(filename, "w") as file:
            json.dump(features, file)
    print(f"GeoJSON-Datei '{filename}' wurde erstellt.")


def import_geojson_to_db():
    # just copy the code from the other script or import that function!
    pass

def fetch_otp_api(cor_dict,url, precision, cutoff, mode, speed, date, time):
    # http://localhost:8080/otp/routers/current/isochrone?algorithm=accSampling&fromPlace=53.59860878,9.99349447&mode=BICYCLE&bikeSpeed=4.916667&date=2024-12-12&time=10:00:00&precisionMeters=10&cutoffSec=900
    results = {}
    error_results = {}


    for table in cor_dict.keys():
        results[table] = []
        error_results[table] = []
        for cor in cor_dict[table]:
            request_url = f"{url}?algorithm=accSampling&fromPlace={cor[0]},{cor[1]}&mode={mode}&bikeSpeed={speed}&date={date}&time={time}&precisionMeters={precision}&cutoffSec={cutoff}"
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

    # input is the dict with the coordinates
    # for each value in the cor list make a request
    # save the response

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

            
            for index, (key, value) in enumerate(fetch_results.items()):
                print(f"{index}: {key} -> {value}")


            for table in fetch_results.keys():
                file_name = "otp_iso_" + table + ".geojson"
                geojson_path = os.path.join(params["geojson_dir"], file_name)
                geojson_data = convert_json_2_geojson(fetch_results, cutoff= cutoff, mode = mode, speed = speed, date = date, time = time, precision = precision, filename = geojson_path)

            
    except Exception as e:
        print(f"Error: {e}")


############################################################################
1. Geojson wird nicht korrekt erstellt, die [] ganz am Anfang und Ende müssen weg
2. Es wird nur ein Polygon eingespeist und nicht alle von Hamburg
3. Ggf vorab nochmal gucken ob die fertigen Punktlayer auch wirklich alle nur im Raum Hamburg sind, sonst ist das ggf. ne Fehlerquelle
4. Import in die DB kann man von set up db nehmen, müsste genau das gleiche sein
################################################################################
with open ("C:\\Master\\GeoinfoPrj_Sem1\\Erreichbarkeitsanalyse\\fetch_data\\fetch_data_config.json", "r") as file:
    config = json.load(file)
params = {
    "url": config["fetch_otp"]["server_url"],
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

