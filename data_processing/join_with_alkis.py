from sqlalchemy import text, inspect
from sqlalchemy.exc import SQLAlchemyError


def handle_conf_join_with_alkis(config):
    join_with_alkis = config["table_processing"]["join_with_alkis"]
    return join_with_alkis

def rename_fields_with_schema(db_con, schemas):
    inspector = inspect(db_con)
    
    for schema in schemas:
        try:
            # Hole alle Tabellen im aktuellen Schema
            tables = inspector.get_table_names(schema=schema)
            
            for table in tables:
                # Neuer Tabellenname für die alte Tabelle
                old_table_name = f"{table}_noRename"
                
                # Umbenennen der Originaltabelle
                with db_con.connect() as connection:
                    try:
                        rename_query = f"ALTER TABLE {schema}.{table} RENAME TO {old_table_name};"
                        connection.execute(text(rename_query))
                        print(f"Tabelle '{table}' wurde erfolgreich in '{old_table_name}' umbenannt.")
                    except SQLAlchemyError as e:
                        print(f"Ein Fehler ist beim Umbenennen der Tabelle '{table}' auf '{old_table_name}' aufgetreten: {e}")
                        continue  # Wenn das Umbenennen fehlschlägt, überspringe diese Tabelle

                # Hole die Spalteninformationen der umbenannten Originaltabelle
                columns = inspector.get_columns(old_table_name, schema=schema)
                
                # Erstelle eine Liste mit den umbenannten Spalten für den SELECT-Teil der Abfrage
                select_columns = [
                    f"\"{col['name']}\" AS \"{schema}_{col['name']}\"" for col in columns
                ]
                
                # Erstellen der SQL-Abfrage zum Erstellen der neuen Tabelle mit umbenannten Spalten und ursprünglichem Namen
                query = f"""
                    CREATE TABLE {schema}.{table} AS
                    SELECT 
                        {', '.join(select_columns)}
                    FROM 
                        {schema}.{old_table_name};
                """
                
                # Debug-Ausgabe der Abfrage, um die generierte SQL-Anweisung zu überprüfen
                print(f"SQL Query for {table}:\n{query}\n")


                # Führe die SQL-Abfrage aus, um die neue Tabelle zu erstellen
                with db_con.connect() as connection:
                    try:
                        connection.execute(text(query))
                        connection.commit()  # WICHTIG: Explizit committen, um die Änderungen zu speichern
                        print(f"Neue Tabelle '{table}' wurde erfolgreich im Schema '{schema}' erstellt.")
                    except SQLAlchemyError as e:
                        print(f"Ein Fehler ist beim Erstellen der Tabelle '{table}' im Schema '{schema}' aufgetreten: {e}")
        
        except SQLAlchemyError as e:
            print(f"Ein Fehler ist beim Abrufen der Tabellen im Schema '{schema}' aufgetreten: {e}")

def join_POI_with_ALKIS(db_con, join_config):
    for schema, alkis_table in join_config.items():
        try:
            # Erstelle eine Verbindung zur Datenbank
            with db_con.connect() as connection:
                # Holen Sie sich alle Tabellen im Quellschema
                inspector = inspect(db_con)
                tables_in_source_schema = inspector.get_table_names(schema=schema)

                for table in tables_in_source_schema:
                    # Bestimme den neuen Tabellennamen basierend auf dem Zieltabellen-Namen
                    if "gebaeude" in alkis_table:
                        new_table_name = f"{table}_IntrsctGEB"
                    elif "flurstueck" in alkis_table:
                        new_table_name = f"{table}_IntrsctFLUR"
                    else:
                        print(f"Ziel-Tabelle '{alkis_table}' muss 'gebaeude' oder 'flurstueck' im Namen enthalten.")
                        continue     

                    try:
                        # Hole die Spalteninformationen für `t1` und `t2`
                        t1_columns = inspector.get_columns(table, schema=schema)
                        t2_columns = inspector.get_columns(alkis_table, schema="flurstuecke")

                        # Erstelle die Spaltenliste für `SELECT` und hänge den Tabellennamen als Präfix an
                        select_columns = [f"t1.{col['name']} AS {table}_{col['name']}" for col in t1_columns]
                        select_columns += [f"t2.{col['name']} AS {alkis_table}_{col['name']}_alkis" for col in t2_columns]

                        # Erstellen der SQL-Abfrage mit der modifizierten Spaltenliste
                        query = f"""
                            CREATE TABLE {schema}.{new_table_name} AS
                            SELECT 
                                {', '.join(select_columns)}
                            FROM 
                                {schema}.{table} AS t1
                            JOIN 
                                flurstuecke.{alkis_table} AS t2
                            ON 
                                ST_Intersects(t1.geometry, t2.geometry);  -- ST_Intersects prüft auf Überschneidung
                        """
                        # Führe die SQL-Abfrage aus
                        connection.execute(text(query))
                        print(f"Tabelle '{new_table_name}' wurde erfolgreich im Schema '{schema}' erstellt.")

                    except SQLAlchemyError as e:
                        print(f"Ein Fehler ist beim Erstellen der Tabelle '{new_table_name}' aufgetreten: {e}")
                        # Rollback der Transaktion, falls Fehler auftritt
                        connection.rollback()
                        
        except SQLAlchemyError as e:
            print(f"Ein Fehler ist beim Abrufen der Tabellen im Schema '{schema}' aufgetreten: {e}")
            connection.rollback()