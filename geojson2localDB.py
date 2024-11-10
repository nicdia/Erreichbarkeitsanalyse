import geopandas
import os
import json
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from util_fcts import connect2DB

# Konfigurationsdatei laden
with open("config.json", "r") as file:
    config = json.load(file)

#######################################################################################
def setup():
    # Verbindung zur Datenbank herstellen
    db_con = connect2DB()
    data = config["geojson2localdb"]["data"]
    config_settings = config["geojson2localdb"]["config"]
    return (data, config_settings, db_con)

def create_schema(data, db_con):
    for schema in data.keys():
        print(f"Erstelle Schema: {schema}")
        try:
            with db_con.connect() as connection:
                # SQL-Anweisung zum Erstellen des Schemas
                query = text(f"CREATE SCHEMA IF NOT EXISTS {schema};")
                connection.execute(query)
                print(f"Schema '{schema}' wurde erfolgreich erstellt.")
        except Exception as e:
            print(f"Fehler beim Erstellen des Schemas '{schema}': {e}")

def create_table_name(data, config):
    file_names_and_path_and_schema = []
    file_formats = config["data_format"]
    for schema, folder_path in data.items():
        for filename in os.listdir(folder_path):
            for file_format in file_formats:
                if filename.endswith(file_format):
                    absolute_path = os.path.join(folder_path, filename)
                    name_without_extension = os.path.splitext(filename)[0]
                    upload_infos = {
                        "name": name_without_extension,
                        "path": absolute_path,
                        "schema": schema
                    }
                    file_names_and_path_and_schema.append(upload_infos)
    return file_names_and_path_and_schema

def upload2db(upload_config, db_con):
    for config in upload_config:
        gdf = geopandas.read_file(config["path"])
        gdf.to_postgis(name=config["name"], con=db_con, schema=config["schema"])
        print(f"The file '{config['name']}' was imported into the database.")

def main_geojson2localdb():
    # Setup und Initialisierung
    data, config_settings, db_con = setup()
    
    # Schema erstellen
    create_schema(data, db_con)
    
    # Tabellennamen und Pfade erzeugen
    table_names_and_paths_and_schema = create_table_name(data, config_settings)
    
    # Dateien in die Datenbank laden
    upload2db(upload_config=table_names_and_paths_and_schema, db_con=db_con)

# Hauptfunktion aufrufen
main_geojson2localdb()