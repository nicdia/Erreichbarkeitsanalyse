from sqlalchemy import create_engine, inspect, text
from sqlalchemy.exc import SQLAlchemyError

def add_column_based_on_table_name(db_con):
    # Verbindung zur Datenbank herstellen
    try:
        # Durch alle Schemas und Tabellen iterieren
        with db_con.connect() as conn:
            # Beginne eine explizite Transaktion
            with conn.begin():
                inspector = inspect(db_con)
                schemas = inspector.get_schema_names()
                
                for schema in schemas:
                    tables = inspector.get_table_names(schema=schema)
                    
                    for table in tables:
                        # Überprüfen, ob "meta" oder "osm" im Tabellennamen vorkommt
                        if "meta" in table:
                            new_column_value = "metaver"
                        elif "osm" in table:
                            new_column_value = "osm"
                        else:
                            continue  # Überspringt Tabellen ohne "meta" oder "osm" im Namen
                        
                        # Prüfen, ob die Spalte bereits existiert
                        columns = [col["name"] for col in inspector.get_columns(table, schema=schema)]
                        if "source" not in columns:
                            # Neue Spalte "source" zur Tabelle hinzufügen
                            alter_query = f'ALTER TABLE "{schema}"."{table}" ADD COLUMN source TEXT;'
                            conn.execute(text(alter_query))
                            print(f"Spalte 'source' zur Tabelle '{schema}.{table}' hinzugefügt.")
                        
                        # Spalte mit dem entsprechenden Wert aktualisieren
                        update_query = f'UPDATE "{schema}"."{table}" SET source = :value;'
                        conn.execute(text(update_query), {"value": new_column_value})
                        print(f"Spalte 'source' in Tabelle '{schema}.{table}' mit Wert '{new_column_value}' aktualisiert.")
    
    except SQLAlchemyError as e:
        print(f"Ein Fehler ist aufgetreten: {e}")

