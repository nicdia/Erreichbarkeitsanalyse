from sqlalchemy import text, Table, select, union_all, inspect
from sqlalchemy.exc import SQLAlchemyError

def handle_conf_union(config):
    union_tables = config["union_data"]
    return union_tables

def union_tables_and_create_table(union_dict, db_con):
    try:
        with db_con.connect() as conn:
            for key, table_list in union_dict.items():
                union_queries = []
                
                for table_name in table_list:
                    table = Table(table_name,autoload_with=db_con)
                    query = select(table)  
                    union_queries.append(query)
            
                # UNION der Abfragen erstellen
                union_query = union_all(*union_queries)
                new_table_name = f"union_{key}"
                
                # CREATE TABLE Query als Text
                create_query = text(f"CREATE TABLE {key}.{new_table_name} AS {union_query}")
                conn.execute(create_query)
                conn.commit()
            
                print(f"Neue Tabelle '{new_table_name}' mit zusammengeführten Daten wurde erfolgreich erstellt.")
    
    except SQLAlchemyError as e:
        print(f"Ein Fehler ist aufgetreten: {e}")


def create_union_table(db_con, schemas):
    # Öffne die Verbindung und starte eine neue Sitzung
    with db_con.connect() as connection:
        inspector = inspect(db_con)

        for schema in schemas:
            # Erstelle den Namen der neuen Union-Tabelle für das aktuelle Schema
            new_table_name = f"{schema}_union"
            
            # Hole alle Tabellen im aktuellen Schema
            tables = inspector.get_table_names(schema=schema)

            # Bestimme alle Spaltennamen, um eine einheitliche Struktur zu schaffen
            all_columns = set()
            for table in tables:
                columns = inspector.get_columns(table, schema=schema)
                all_columns.update([col['name'] for col in columns])

            # Sortiere die Spalten alphabetisch, um Konsistenz in der UNION zu gewährleisten
            all_columns = sorted(all_columns)
            union_queries = []

            # Erstelle eine UNION ALL Abfrage für jede Tabelle
            for table in tables:
                # Hole die tatsächlichen Spalten der aktuellen Tabelle
                actual_columns = {col['name'] for col in inspector.get_columns(table, schema=schema)}

                # Füge eine Spalte hinzu, wenn sie existiert, ansonsten füge NULL hinzu und caste alles auf TEXT
                select_clause = ", ".join([
                    f"CAST({col} AS TEXT) AS {col}" if col in actual_columns else f"NULL AS {col}"
                    for col in all_columns
                ])

                # Erstelle die SELECT-Abfrage mit allen Spalten und der zusätzlichen Quelle
                union_queries.append(
                    f"SELECT '{table}' AS source_table, {select_clause} FROM {schema}.{table}"
                )

            # Baue die finale UNION ALL Abfrage für das aktuelle Schema
            union_query = " UNION ALL ".join(union_queries)
            create_table_query = f"CREATE TABLE {new_table_name} AS {union_query};"

            # Führe die Abfrage aus, um die neue Union-Tabelle zu erstellen
            try:
                connection.execute(text(create_table_query))
                print(f"Tabelle '{new_table_name}' erfolgreich erstellt.")
            except Exception as e:
                print(f"Fehler beim Erstellen der Tabelle '{new_table_name}': {e}")