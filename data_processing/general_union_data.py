from sqlalchemy import inspect, text
from sqlalchemy.exc import SQLAlchemyError

def handle_conf_union(config):
    union_config = config["table_processing"]["union_data"]
    return union_config

from sqlalchemy import text, inspect
from sqlalchemy.exc import SQLAlchemyError

def union_tables(db_con, union_config):
    """
    Unioniert Tabellen eines Schemas und nimmt nur bestimmte Felder. Welche Felder in welcher Tabelle genommen werden und zu welchem Schema die gehören muss vorab in der config_data_processing.json config angegeben werden 

    Args:
        db_con: SQLAlchemy-Datenbankverbindung.
        union_config: Dictionary mit Schema, Tabellen und den zu wählenden Feldern.
    """
    with db_con.connect() as connection:
        for schema, tables in union_config.items():
            print(f"Processing schema: {schema}")
            union_queries = []
            union_table_name = f"{schema}_union"  
            
            for table_name, fields in tables.items():
                if not fields:
                    print(f"No fields specified for table {table_name}, skipping.")
                    continue

                # Erstelle den SELECT-Teil der Query basierend auf den Feldern
                field_list = ", ".join(fields)
                query = f"SELECT {field_list} FROM {schema}.{table_name}"
                union_queries.append(query)

            if not union_queries:
                print(f"No valid tables found in schema: {schema}")
                continue

            # UNION ALL der Abfragen
            union_all_query = " UNION ALL ".join(union_queries)

            # Kompletten Query ausführen
            complete_query = text(f"""
            CREATE TABLE {schema}.{union_table_name} AS
            SELECT * FROM (
                {union_all_query}
            ) AS union_result;
            """)

            print(f"Executing UNION query for schema {schema}...")
            try:
                result = connection.execute(complete_query)
                connection.commit()

            except SQLAlchemyError as e:
                print(f"An error occurred while processing schema {schema}: {e}")