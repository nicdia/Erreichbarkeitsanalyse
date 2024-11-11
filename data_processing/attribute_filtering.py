from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

def handle_conf_attrfilter(config):
    attribute_filtering = config["table_processing"]["attribute_filtering"]
    return attribute_filtering


def filter_and_create_table(filter_settings, db_con):
    required_keys = ["attribute", "value", "new_table_name"]

    for schema, table_dict in filter_settings.items():
        for table_name, config in table_dict.items():
            if not all(key in config and config[key] for key in required_keys):
                print(f"Warnung: '{table_name}' in Schema '{schema}' übersprungen, da notwendige Konfiguration fehlt oder leer ist.")
                continue  
            try:
                query = f"""
                CREATE TABLE {schema}.{config["new_table_name"]} AS
                SELECT * FROM {schema}.{table_name}
                WHERE {config["attribute"]} = :value
                """
                
                with db_con.connect() as conn:
                    conn.execute(text(query), {"value": config["value"]})
                    conn.commit()
                
                print(f"Neue Tabelle '{config['new_table_name']}' wurde erfolgreich erstellt.")
            
            except SQLAlchemyError as e:
                print(f"Ein Fehler ist aufgetreten bei Tabelle '{config['new_table_name']}': {e}")




