from sqlalchemy import text, inspect
from sqlalchemy.exc import SQLAlchemyError
import re


def handle_conf_join_with_alkis(config):
    join_with_alkis = config["table_processing"]["join_with_alkis"]
    return join_with_alkis

def rename_fields_with_schema(db_con, schemas):
    inspector = inspect(db_con)
    
    for schema in schemas:
        try:
            tables = inspector.get_table_names(schema=schema)
            for table in tables:
                columns = inspector.get_columns(table, schema=schema)
                rename_queries = []
                for column in columns:
                    if column['name'] != 'geometry':
                        old_column_name = column['name']
                        if re.search(r'[^a-zA-Z0-9_]', old_column_name):
                            new_column_name = re.sub(r'[^a-zA-Z0-9_]', '_', old_column_name)
                        else:
                            new_column_name = f"{old_column_name}_{table}"
                        rename_queries.append(
        f'ALTER TABLE "{schema}"."{table}" RENAME COLUMN "{old_column_name}" TO "{new_column_name}";'
    )

                # Führe die SQL-Abfrage aus, um die neue Tabelle zu erstellen
                with db_con.connect() as connection:
                    try:
                        for query in rename_queries:
                            connection.execute(text(query))
                            connection.commit() 
                            print(f"Das Feld '{old_column_name}' im Schema '{schema}' wurde erfolgreich umbenannt.")
                    except SQLAlchemyError as e:
                        print(f"Ein Fehler ist beim Erstellen der Tabelle '{table}' im Schema '{schema}' aufgetreten: {e}")

                        
        
        except SQLAlchemyError as e:
            print(f"Ein Fehler ist beim Abrufen der Tabellen im Schema '{schema}' aufgetreten: {e}")

def join_POI_with_ALKIS(db_con, join_config):
    for schema, alkis_table in join_config.items():
        try:
            # Verbindung zur Datenbank öffnen
            with db_con.connect() as connection:
                # Aktiviert die Transaktion
                transaction = connection.begin()
                try:
                    # Prüfe alle Tabellen im Quellschema
                    inspector = inspect(db_con)
                    tables_in_source_schema = inspector.get_table_names(schema=schema)

                    for table in tables_in_source_schema:
                        # Bestimme neuen Tabellennamen
                        if "gebaeude" in alkis_table:
                            new_table_name = f"{table}_IntrsctGEB"
                        elif "flurstueck" in alkis_table:
                            new_table_name = f"{table}_IntrsctFLUR"
                        else:
                            print(f"Ungültige Ziel-Tabelle '{alkis_table}': Muss 'gebaeude' oder 'flurstueck' enthalten.")
                            continue

                        try:
                            # Prüfe, ob beide Tabellen existieren
                            if not inspector.has_table(table, schema=schema):
                                print(f"Tabelle '{schema}.{table}' existiert nicht, überspringe.")
                                continue
                            if not inspector.has_table(alkis_table, schema="flurstuecke"):
                                print(f"Tabelle 'flurstuecke.{alkis_table}' existiert nicht, überspringe.")
                                continue

                            # Hole die Spalteninformationen
                            t1_columns = inspector.get_columns(table, schema=schema)
                            t2_columns = inspector.get_columns(alkis_table, schema="flurstuecke")

                            # Prüfe, ob Geometry-Spalten existieren
                            if not any(col['name'] == "geometry" for col in t1_columns):
                                print(f"Tabelle '{schema}.{table}' hat keine 'geometry'-Spalte, überspringe.")
                                continue
                            if not any(col['name'] == 'geometry' for col in t2_columns):
                                print(f"Tabelle 'flurstuecke.{alkis_table}' hat keine 'geometry'-Spalte, überspringe.")
                                continue

                            # Erstelle die Spaltenliste für den SELECT-Teil
                            select_columns = [f"t1.{col['name']} AS {table}_{col['name']}" for col in t1_columns]
                            select_columns += [f"t2.{col['name']} AS {alkis_table}_{col['name']}_alkis" for col in t2_columns]

                            # SQL-Abfrage erstellen
                            query = f"""
                                CREATE TABLE {schema}.{new_table_name} AS
                                SELECT 
                                    {', '.join(select_columns)}
                                FROM 
                                    {schema}.{table} AS t1
                                JOIN 
                                    flurstuecke.{alkis_table} AS t2
                                ON 
                                    ST_Intersects(t1.geometry, t2.geometry);
                            """

                            # SQL-Abfrage ausführen
                            connection.execute(text(query))
                            print(f"Tabelle '{new_table_name}' wurde erfolgreich im Schema '{schema}' erstellt.")

                        except SQLAlchemyError as e:
                            print(f"Fehler beim Erstellen der Tabelle '{schema}.{new_table_name}': {e}")
                            continue

                    # Commit nach der erfolgreichen Verarbeitung eines Schemas
                    transaction.commit()
                    print(f"Änderungen im Schema '{schema}' wurden erfolgreich gespeichert.")

                except SQLAlchemyError as e:
                    # Rollback bei Fehlern
                    print(f"Fehler bei der Verarbeitung im Schema '{schema}': {e}")
                    transaction.rollback()
        except SQLAlchemyError as e:
            print(f"Fehler beim Verbinden mit der Datenbank: {e}")