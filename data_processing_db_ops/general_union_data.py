from sqlalchemy import inspect, text
from sqlalchemy.exc import SQLAlchemyError

def handle_conf_union(config):
    union_config = config["table_processing"]["union_data"]
    return union_config



def union_tables(db_con, union_config):
    """
    Unioniert Tabellen eines Schemas und nimmt nur bestimmte Felder. Die Konfiguration muss vorab 
    angeben, welche Felder aus welchen Tabellen genommen werden und wie sie einheitlich benannt werden. Links ist der Alias Name in der Query und rechts muss der Feldname genommen werden, der Inhalt wird dann entsprechend zusammengepackt mit den anderen Feldinhalten. Also das macht Sinn bei Namensfeldern aber nicht bei Namen-Alias das Geometry Field angeben!

    Args:
        db_con: SQLAlchemy-Datenbankverbindung.
        union_config: Dictionary mit Schema, Tabellen und den zu wählenden Feldern. 
                      Beispiel:
                      {
                          "schema_name": {
                              "table1": {"name": "col1", "source": "col2", "geom": "geom_col"},
                              "table2": {"name": "name_field", "source": "src_field", "geom": "geometry"},
                          }
                      }
    """
    with db_con.connect() as connection:
        for schema, tables in union_config.items():
            print(f"Processing schema: {schema}")
            union_queries = []
            union_table_name = f"{schema}_union"
            
            for table_name, field_mapping in tables.items():
                if not field_mapping:
                    print(f"No fields specified for table {table_name}, skipping.")
                    continue

                # Erstelle die SELECT-Abfrage mit Aliassen basierend auf der Konfiguration
                select_parts = []
                for unified_field, source_field in field_mapping.items():
                    select_parts.append(f"{source_field} AS {unified_field}")
                field_list = ", ".join(select_parts)

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
                print(f"Successfully created table {schema}.{union_table_name}")
            except SQLAlchemyError as e:
                print(f"An error occurred while processing schema {schema}: {e}")