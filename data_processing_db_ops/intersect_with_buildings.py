from sqlalchemy import create_engine, text

def handle_conf_intersect(config):
    intersect_config = config["table_processing"]["isochrone_building_intersection"]
    return intersect_config

def get_geometry_column(conn, schema, table_name):
    """
    Prüft, wie die Geometriespalte in einer Tabelle heißt.
    """
    result = conn.execute(text(f"""
        SELECT column_name
        FROM information_schema.columns
        WHERE table_schema = :schema AND table_name = :table
        AND udt_name = 'geometry';
    """), {"schema": schema, "table": table_name}).fetchone()
    return result[0] if result else None

def intersect_buildings_isochrones(intersect_settings, db_con):

    target_schema = intersect_settings["target_schema"]
    source_schema = intersect_settings["source_schema"]
    wohngebaeude_table = intersect_settings["wohngebaeude_table"]
    wohngebaeude_schema, wohngebaeude_table_name = wohngebaeude_table.split(".")
    
    with db_con.connect() as conn:
        try:
            # Ziel-Schema erstellen, falls nicht vorhanden
            conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS {target_schema};"))

            # Geometriespalte der Wohngebäude-Tabelle ermitteln
            wohngebaeude_geom_col = "geometry"

            # Alle Tabellen im Quellschema abrufen
            tables = conn.execute(text(f"""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = :schema
            """), {"schema": source_schema}).fetchall()

            # Iteration über alle Tabellen
            for table in tables:
                table_name = table[0]

                # Geometriespalte der Isochronen-Tabelle ermitteln
                isochrone_geom_col = get_geometry_column(conn, source_schema, table_name)
                if not isochrone_geom_col:
                    print(f"Überspringe Tabelle {table_name}, da keine Geometriespalte gefunden wurde.")
                    continue

                # Neuer Tabellenname für transformierte Daten
                transformed_table = f"{table_name}_25832"

                # SRID-Transformation durchführen und neue Tabelle erstellen
                print(f"Transformiere Tabelle: {table_name} -> {transformed_table}")
                conn.execute(text(f"""
                CREATE TABLE {source_schema}.{transformed_table} AS
                SELECT 
                    ST_Transform({isochrone_geom_col}, 25832) AS geometry  -- Nur transformierte Geometrie behalten
                FROM {source_schema}.{table_name};
            """))

                # Intersect-Query ausführen und Ergebnisse speichern
                intersect_table = f"{target_schema}.intersect_{table_name}"
                print(f"Erstelle Intersect-Tabelle: {intersect_table}")
                conn.execute(text(f"""
                    CREATE TABLE {intersect_table} AS
                    SELECT 
                        geb.*
                    FROM {wohngebaeude_table} geb
                    JOIN {source_schema}.{transformed_table} iso
                    ON ST_Intersects(geb.{wohngebaeude_geom_col}, iso.geometry);
                """))

                # Index auf der Ergebnis-Tabelle erstellen (optional für Performance)
                print(f"Erstelle Index für Tabelle: {intersect_table}")
                conn.execute(text(f"""
                    CREATE INDEX idx_{table_name}_geom ON {intersect_table} USING GIST(geometry);
                """))
            conn.commit()
            print("Alle Tabellen wurden transformiert und Intersect-Operationen abgeschlossen.")
        except Exception as e:
                conn.rollback() 
                print(f"Ein Fehler ist aufgetreten: {e}")


def duplicate_building_layer(db_con, prefix_new_table, target_schema, wohngebaeude_table,wohngebaeude_table_name):
    new_table_name = f"{prefix_new_table}_{wohngebaeude_table_name}"
    new_table_full_name = f"{target_schema}.{new_table_name}"

    copy_query = text(f"""
    CREATE TABLE {new_table_full_name} AS
    SELECT * FROM {wohngebaeude_table};
    """)
    db_con.execute(copy_query)
    return new_table_full_name

def get_field_name(table):
    # the table names in the db need to have the name format like this: intersect_bicycle_iso_17_7km_ausserschulisch
    # the function will return this part: bicycle_iso_17_7km_ausserschulisch
    extracted_name = table.split('_',1)[1]
    return extracted_name

def extract_mode_and_settings_from_field_name(field_name):
    # the input field name needs to have a structure like this: bicycle_iso_17_7km_ausserschulisch
    # it will return this part: bicycle_iso_17_7km
    mode_and_settings = field_name.rsplit('_', 1)[0]
    return mode_and_settings

def get_tables(schema, db_con):
    fetch_tables_query = text(f"""
    SELECT table_name
    FROM information_schema.tables
    WHERE table_schema = :schema;
    """)
    # they have the wrong type: <class 'sqlalchemy.engine.row.Row'>
    sql_results_tables = db_con.execute(fetch_tables_query, {"schema": schema}).fetchall()
    # the type is now <class 'str'>
    only_string_names = [row[0] for row in sql_results_tables]
    return only_string_names

def create_intersect_counting_field(duplicated_building_layer, db_con, new_field_name):
    alter_query = text(f"""
    ALTER TABLE {duplicated_building_layer}
    ADD COLUMN {new_field_name} INTEGER DEFAULT 0;
    """)
    db_con.execute(alter_query)

def add_intersect_feature_count(table_name, schema_name, wohngebaeude_table, field_name, db_con):
    """
    Prüft für jedes Feature in der wohngebaeude_table, ob es in der source_table vorhanden ist,
    und erhöht das Integer-Feld um 1, wenn dies der Fall ist.

    Args:
        table_name (str): Name der Tabelle, die geprüft werden soll.
        schema_name (str): Name des Schemas, in dem die Tabelle "table_name" liegt.
        wohngebaeude_table (str): Name der Tabelle, in der die Spalte "field_name" liegt.
        field_name (str): Name der Spalte, die erhöht werden soll.
        db_con (sqlalchemy.engine.Engine): Datenbankverbindung.
    """
    print(f"This is the input table name: {table_name}")
    print(f"This is the input schema name: {schema_name}")

    source_table_full_name = f"{schema_name}.{table_name}"

    update_query = text(f"""
    UPDATE {wohngebaeude_table} AS target
    SET {field_name} = {field_name} + 1
    WHERE EXISTS (
        SELECT 1
        FROM {source_table_full_name} AS source
        WHERE ST_Intersects(target.geometry, source.geometry)
    );
    """)
    db_con.execute(update_query)

def execute_intersect_count_adding(intersect_settings, db_con, prefix_new_table):

    # target_schema = intersect_results
    intersect_results_schema = intersect_settings["target_schema"]
    # wohngebaeude_table = flurstuecke.wohngebaeude
    original_wohngebaeude_table = intersect_settings["wohngebaeude_table"]
    wohngebaeude_schema, wohngebaeude_table_name = original_wohngebaeude_table.split(".")
    with db_con.connect() as conn:
        try:
            created_fields = []
            duplicated_layer = duplicate_building_layer(conn, prefix_new_table, wohngebaeude_schema, original_wohngebaeude_table, wohngebaeude_table_name)
            tables = get_tables(schema = intersect_results_schema, db_con= conn)
            print (f"this is al tables in execute: {tables}")
            for table in tables:
                field_name = get_field_name(table)
                mode_and_settings = extract_mode_and_settings_from_field_name(field_name)
                print (f"this is field name that will be used: {mode_and_settings}")
                if mode_and_settings not in created_fields:
                    create_intersect_counting_field(duplicated_building_layer=duplicated_layer,db_con=conn, new_field_name=mode_and_settings)
                    created_fields.append(mode_and_settings)
            print (f"this is the current created fields: {created_fields}")
            for table in tables:
                for created_field in created_fields:
                    if created_field in table:
                        # created field looks for example like this: bicycle_iso_17_7km
                        # table name looks for example like this: intersect_bicycle_iso_17_7km_ausserschulisch
                        print (f"MATCH: {table} count will be added in field {created_field}")
                        add_intersect_feature_count(schema_name=intersect_results_schema,table_name = table, wohngebaeude_table=duplicated_layer, field_name=created_field, db_con=conn)
                        print (f"count was added for {table} in field {mode_and_settings}")
                    else:
                        print (f"NO MATCH:{table} and {created_field}")


            print(f"Intersect Count Adding completed for {duplicated_layer}.")
            conn.commit()


        
        except Exception as e:
                conn.rollback() 
                print(f"Ein Fehler ist aufgetreten: {e}")
