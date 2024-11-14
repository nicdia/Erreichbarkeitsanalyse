import geopandas
import os
import json
from sqlalchemy import create_engine, text
from util_fcts import setup



#######################################################################################

def handle_config_settings(config):
    """
    Extrahiert die Konfigurationseinstellungen fuer die geojson2localdb-Funktion aus dem config-Objekt.
    
    Parameters:
    config (dict): Enthaelt die Konfigurationseinstellungen fuer die geojson2localdb-Funktion.
    
    Returns:
    tuple: Enthaelt die Konfigurationseinstellungen fuer die geojson2localdb-Funktion.
    """
    data = config["geojson2localdb"]["data"]
    config_settings = config["geojson2localdb"]["config"]
    return (data, config_settings)

def create_schema(data, db_con):
    """
    Erstellt die angegebenen Schemata in der Datenbank, falls sie noch nicht existieren.

    Parameters:
    data (dict): Dict mit Schema-Namen als Key und ordnerpfad als Value.
    db_con (sqlalchemy.engine.Engine): Verbindungsobjekt zur Datenbank
    """
    
    for schema in data.keys():
        print(f"Erstelle Schema: {schema}")
        try:
            # Using a transaction to ensure the schema creation is committed
            with db_con.begin() as connection:
                # SQL-Anweisung zum Erstellen des Schemas
                query = text(f"CREATE SCHEMA IF NOT EXISTS {schema};")
                connection.execute(query)
                print(f"Schema '{schema}' wurde erfolgreich erstellt.")
        except Exception as e:
            print(f"Fehler beim Erstellen des Schemas '{schema}': {e}")

def create_table_name(data, config):
    """
    Erstellt eine Liste von Dateinamen, Pfaden und zugehoerigem Schema fuer die Dateien, die in den Ordnern
    unterhalb des angegebenen `data`-Objekts gefunden werden. Die Dateien werden nach dem Schema,
    das im `data`-Objekt fuer den Ordner definiert wird, gruppiert.

    Parameters:
    data (dict): Dict mit Schema-Namen als Key und Ordnerpfad als Value.
    config (dict): Dict mit Konfigurationseinstellungen fuer die geojson2localdb-Funktion.

    Returns:
    list: Liste mit Dateinamen, Pfaden und zugehoerigem Schema fuer die Dateien, die in den Ordnern
    unterhalb des angegebenen `data`-Objekts gefunden werden.
    """
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
    """
    Importiert die Dateien, die in der Liste `upload_config` enthalten sind,
    in die Datenbank. Jedes Element der Liste muss ein Dict mit den
    folgenden Keys enthalten:
    - "name": Der Name der Tabelle, in die die Datei importiert werden soll
    - "path": Der absolute Pfad zu der Datei
    - "schema": Der Name des Schemas, in dem die Tabelle erstellt werden soll

    Parameters:
    upload_config (list): Liste von Dicts mit den Import-Informationen
    db_con (sqlalchemy.engine.Engine): Verbindung zur Datenbank
    """
    for config in upload_config:
        gdf = geopandas.read_file(config["path"])
        gdf.to_postgis(name=config["name"], con=db_con, schema=config["schema"])
        print(f"The file '{config['name']}' was imported into the database.")

def main_geojson2localdb(db_con, config):
    """
    Liest die Konfiguration fuer die geojson2localdb-Funktion aus einem dict aus und fuehrt die
    Funktionen zur Erstellung der Schemata und zum Import der Dateien in die Datenbank aus.

    Parameters:
    db_con (sqlalchemy.engine.Engine): Verbindung zur Datenbank
    config (dict): Dict mit Konfigurationseinstellungen fuer die geojson2localdb-Funktion

    Returns:
    list: Liste von Dicts mit den Import-Informationen
    """
    data, config_settings = handle_config_settings(config)
    # Schema erstellen
    create_schema(data, db_con)
    
    # Tabellennamen und Pfade erzeugen
    table_names_and_paths_and_schema = create_table_name(data, config_settings)
    
    # Dateien in die Datenbank laden
    upload2db(upload_config=table_names_and_paths_and_schema, db_con=db_con)

    return table_names_and_paths_and_schema
