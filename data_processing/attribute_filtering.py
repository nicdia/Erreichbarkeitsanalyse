from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

def handle_conf_attrfilter(config):
    attribute_filtering = config["table_processing"]["attribute_filtering"]
    return attribute_filtering


def filter_and_create_table(filter_settings, db_con):
    required_keys = ["attribute", "value", "new_table_name"]
    for schema, table_dict in filter_settings.items():
        # Altes Schema umbenennen und neues Schema mit dem ursprünglichen Namen erstellen
        old_schema_name = f"{schema}_not_attr_filtered"
        
        try:
            with db_con.connect() as conn:
                # Schema umbenennen
                conn.execute(text(f"ALTER SCHEMA {schema} RENAME TO {old_schema_name};"))
                print(f"Schema '{schema}' erfolgreich in '{old_schema_name}' umbenannt.")
                
                # Neues Schema mit dem ursprünglichen Namen erstellen
                conn.execute(text(f"CREATE SCHEMA {schema};"))
                print(f"Neues Schema '{schema}' erstellt.")
                conn.commit()
        except SQLAlchemyError as e:
            print(f"Ein Fehler ist beim Umbenennen oder Erstellen des Schemas '{schema}' aufgetreten: {e}")
            continue  # Wenn das Schema nicht umbenannt werden konnte, fahre mit dem nächsten Schema fort

        # Tabellen in diesem Schema verarbeiten
        for table_name, config in table_dict.items():
            if not all(key in config and config[key] for key in required_keys):
                print(f"Warnung: '{table_name}' in Schema '{schema}' übersprungen, da notwendige Konfiguration fehlt oder leer ist.")
                continue  

            try:
                # Abfrage erstellen, um die gefilterte Tabelle im neuen Schema zu erstellen
                query = f"""
                CREATE TABLE {schema}.{config["new_table_name"]} AS
                SELECT * FROM {old_schema_name}.{table_name}
                WHERE {config["attribute"]} = :value
                """
                
                with db_con.connect() as conn:
                    conn.execute(text(query), {"value": config["value"]})
                    conn.commit()
                
                print(f"Neue Tabelle '{config['new_table_name']}' wurde erfolgreich im Schema '{schema}' erstellt.")
            
            except SQLAlchemyError as e:
                print(f"Ein Fehler ist aufgetreten bei Tabelle '{config['new_table_name']}' in Schema '{schema}': {e}")



def custom_ALKIS_building_filtering(db_con):
    query = """
CREATE TABLE flurstuecke.wohngebaeude AS
SELECT funktion, aktualit, geometry
FROM flurstuecke."gebaeude_alkis"
WHERE funktion = 'Wohnhaus'
OR funktion = 'Gebäude für Gewerbe und Industrie mit Wohnen'
OR funktion = 'Gebäude für Handel und Dienstleistungen mit Wohnen'
OR funktion = 'Gemischt genutztes Gebäude mit Wohnen'
OR funktion = 'Land- und forstwirtschaftliches Wohngebäude'
OR funktion = 'Land- und forstwirtschaftliches Wohn- und Betriebsgebäude'
OR funktion = 'Wohngebäude mit Gemeinbedarf'
OR funktion = 'Wohngebäude mit Gewerbe und Industrie'
OR funktion = 'Wohngebäude mit Handel und Dienstleistungen'
OR funktion = 'Wohnheim';
"""
    try:
        with db_con.connect() as connection:
            connection.execute(text(query))
            connection.commit()  
            print("Die Tabelle 'wohngebaeude' wurde erfolgreich erstellt.")
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")
