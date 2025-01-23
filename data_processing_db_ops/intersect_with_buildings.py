from sqlalchemy import text
import re

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

def transform_otp_fetch_to_25832(intersect_settings, db_con):
    source_schema = intersect_settings[0]["source_schema"]
    with db_con.connect() as conn:
        try:
            tables = conn.execute(text(f"""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = :schema
            """), {"schema": source_schema}).fetchall()
            for table in tables:
                table_name = table[0]
                print (f"THIS IS TABLE NAME {table_name}")
                # Geometriespalte der Isochronen-Tabelle ermitteln
                isochrone_geom_col = get_geometry_column(conn, source_schema, table_name)
                if not isochrone_geom_col:
                    print(f"Überspringe Tabelle {table_name}, da keine Geometriespalte gefunden wurde.")
                    continue
                transformed_table = f"{table_name}_25832"
                existing_table = conn.execute(text(f"""
                    SELECT EXISTS (
                        SELECT 1 
                        FROM information_schema.tables 
                        WHERE table_schema = :schema AND table_name = :table
                    );
                """), {"schema": source_schema, "table": transformed_table}).scalar()

                if not existing_table:
                    print(f"Transformiere Tabelle: {table_name} -> {transformed_table}")
                    conn.execute(text(f"""
                        CREATE TABLE {source_schema}.{transformed_table} AS
                        SELECT 
                            ST_Transform({isochrone_geom_col}, 25832) AS geometry  -- Nur transformierte Geometrie behalten
                        FROM {source_schema}.{table_name};
                    """))
                    conn.commit()
                else:
                    print(f"Tabelle {transformed_table} existiert bereits, überspringe Transformation.")
        except Exception as e:
            conn.rollback() 
            print(f"Ein Fehler ist aufgetreten: {e}")

def intersect_buildings_isochrones(intersect_settings, db_con):

    target_schema = intersect_settings["target_schema"]
    source_schema = intersect_settings["source_schema"]
    wohngebaeude_table = intersect_settings["wohngebaeude_table"]
    score_system = intersect_settings["score_system"]
    # keyword for each run with specific score systems
    keyword = intersect_settings["keyword"]

    
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
                if "_25832" in table_name:
                    table_name_no_srs = table_name.replace("_25832", "")
                    intersect_table = f"{target_schema}.intersect_{table_name_no_srs}_{keyword}"
                    existing_intersect_table = conn.execute(text(f"""
                        SELECT EXISTS (
                            SELECT 1 
                            FROM information_schema.tables 
                            WHERE table_schema = :schema AND table_name = :table
                        );
                    """), {"schema": target_schema, "table":intersect_table}).scalar()

                    if not existing_intersect_table:
                        print(f"Erstelle Intersect-Tabelle: {intersect_table}")
                        conn.execute(text(f"""
                            CREATE TABLE {intersect_table} AS
                            SELECT 
                                geb.*
                            FROM {wohngebaeude_table} geb
                            JOIN {source_schema}.{table_name} iso
                            ON ST_Intersects(geb.{wohngebaeude_geom_col}, iso.geometry);
                        """))

                        # Index auf der Ergebnis-Tabelle erstellen (optional für Performance)
                        print(f"Erstelle Index für Tabelle: {intersect_table}")
                        conn.execute(text(f"""
                            CREATE INDEX idx_{table_name}_geom ON {intersect_table} USING GIST(geometry);
                        """))
                    else:
                        print(f"Intersect-Tabelle {intersect_table} existiert bereits, überspringe Erstellung.")
            conn.commit()
            print("Alle Tabellen wurden transformiert und Intersect-Operationen abgeschlossen.")
        except Exception as e:
                conn.rollback() 
                print(f"Ein Fehler ist aufgetreten: {e}")


def duplicate_building_layer(db_con, prefix_new_table, target_schema, wohngebaeude_table, wohngebaeude_table_name):
    new_table_name = f"{prefix_new_table}_{wohngebaeude_table_name}"
    new_table_full_name = f"{target_schema}.{new_table_name}"

    # Query to check if the table exists
    check_query = text(f"""
    SELECT EXISTS (
        SELECT 1 
        FROM information_schema.tables 
        WHERE table_schema = '{target_schema}' 
          AND table_name = '{new_table_name}'
    );
    """)

    # Check if the table exists
    result = db_con.execute(check_query).fetchone()

    if result[0]:  # If the table exists
        print(f"Table {new_table_full_name} already exists.")
        return new_table_full_name

    # If the table does not exist, create it
    copy_query = text(f"""
    CREATE TABLE {new_table_full_name} AS
    SELECT * FROM {wohngebaeude_table};
    """)
    db_con.execute(copy_query)
    print(f"Table {new_table_full_name} created.")
    return new_table_full_name

def get_field_name(table):
    # the table names in the db need to have the name format like this: intersect_bicycle_iso_17_7km_ausserschulisch
    # the function will return this part: bicycle_iso_17_7km_ausserschulisch
    extracted_name = table.split('_',1)[1]
    return extracted_name

def extract_mode_and_settings_from_field_name(field_name):
    # the input field name needs to have a structure like this: bicycle_iso_17_7km_ausserschulisch
    # it will return this part: bicycle_iso_17_7km
    print ("gets here 4")
    test = field_name.rsplit('_', 2)[0]
    print ("test")
    print (test)
    mode_and_settings = field_name.rsplit('_', 2)[0]
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

def create_intersect_counting_field(duplicated_building_layer, db_con, new_aggregated_field_name):
    alter_query = text(f"""
    ALTER TABLE {duplicated_building_layer}
    ADD COLUMN {new_aggregated_field_name} INTEGER DEFAULT 0;
    """)

    ## to be implemented ##
    # for each aggregated count field, create 8 more indicator fields, and for each write if that feature is in the isochrone table or not --> bool
    db_con.execute(alter_query)
    print (f"Created new field: {new_aggregated_field_name}")

def create_indicator_boolean_fields (duplicated_building_layer, db_con, field_name):
    alter_boolean_query = text(f"""
    ALTER TABLE {duplicated_building_layer}
    ADD COLUMN {field_name} BOOLEAN DEFAULT FALSE;
    """)
    db_con.execute(alter_boolean_query)
    print(f"Boolean field {field_name} was created.")



def extract_increment_factor(table_name, score_dict):
    # take the table name string
    for key in score_dict:
        if key in table_name:
            return score_dict[key]
    print (f"WARNING: No increment factor found for table: {table_name}. Check the score system in your config and the names of your tables in db.")
    return None
    # check if  a key of score dict is in the string
    # for that key return the value

def add_intersect_boolean_values(table_name, schema_name, wohngebaeude_table, db_con, field_name):
    source_table_full_name = f"{schema_name}.{table_name}"
    update_query = text(f"""
UPDATE {wohngebaeude_table} AS target
SET {field_name} = EXISTS (
    SELECT 1
    FROM {source_table_full_name} AS source
    WHERE ST_Intersects(target.geometry, source.geometry)
);
""")
    db_con.execute(update_query)

def add_intersect_feature_count(table_name, schema_name, wohngebaeude_table, field_name, db_con, score_factor):
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

    source_table_full_name = f"{schema_name}.{table_name}"

    update_query = text(f"""
    UPDATE {wohngebaeude_table} AS target
    SET {field_name} = {field_name} + {score_factor}
    WHERE EXISTS (
        SELECT 1
        FROM {source_table_full_name} AS source
        WHERE ST_Intersects(target.geometry, source.geometry)
    );
    """)
    db_con.execute(update_query)

def does_field_match_table(created_field, table):
    # table = intersect_bicycle_iso_4_916667km_ausserschulangebote_54311223 created_field = bicycle_iso_4_916667km_54311223
    table_first_part, table_keyword_part = table.rsplit('_', 1) 
    field_first_part, field_keyword_part = created_field.rsplit('_', 1)
    if table_keyword_part == field_keyword_part and field_first_part in table_first_part:
        return True
    else:
        return False
    

def execute_intersect_count_adding(intersect_settings, db_con, prefix_new_table):

    # target_schema = intersect_results
    intersect_results_schema = intersect_settings["target_schema"]
    # wohngebaeude_table = flurstuecke.wohngebaeude
    original_wohngebaeude_table = intersect_settings["wohngebaeude_table"]
    wohngebaeude_schema, wohngebaeude_table_name = original_wohngebaeude_table.split(".")

    #score system is a dict
    score_system = intersect_settings["score_system"]
    # keyword for each run with specific score systems
    keyword = intersect_settings["keyword"]


    with db_con.connect() as conn:
        try:
            created_aggregated_fields = []
            created_boolean_fields = []
            duplicated_layer = duplicate_building_layer(conn, prefix_new_table, wohngebaeude_schema, original_wohngebaeude_table, wohngebaeude_table_name)
            tables = get_tables(schema = intersect_results_schema, db_con= conn)
            print (f"this is all tables in execute: {tables}")

            for table in tables:
                field_name = get_field_name(table)
                mode_and_settings = extract_mode_and_settings_from_field_name(field_name)
                aggregated_field_name = mode_and_settings +"_"+ keyword
                boolean_field_name = field_name 
                if aggregated_field_name not in created_aggregated_fields:
                    create_intersect_counting_field(duplicated_building_layer=duplicated_layer,db_con=conn, new_aggregated_field_name=aggregated_field_name)
                    created_aggregated_fields.append(aggregated_field_name)
                create_indicator_boolean_fields(duplicated_building_layer=duplicated_layer, db_con=conn,field_name = boolean_field_name)
                created_boolean_fields.append(boolean_field_name)
            print (f"this is all created aggregated fields: {created_aggregated_fields}")
            print (f"this is all created boolean fields: {created_boolean_fields}")
            for table in tables:
                for created_field in created_aggregated_fields:
                    if does_field_match_table(created_field, table):
                        print (f"MATCH AGGREGATED: {table} count will be added in field {created_field}")
                        score_factor = extract_increment_factor(table, score_system)
                        add_intersect_feature_count(schema_name=intersect_results_schema,table_name = table, wohngebaeude_table=duplicated_layer, field_name=created_field, db_con=conn, score_factor=score_factor)
                    else:
                        print (f"NO MATCH AGGREGATED:{table} and {created_field}")
                for created_field in created_boolean_fields:
                    if created_field in table:
                        print (f"MATCH BOOLEAN: {table} boolean will be added in field {created_field}")
                        add_intersect_boolean_values(schema_name=intersect_results_schema,table_name = table, wohngebaeude_table=duplicated_layer, field_name=created_field, db_con=conn)
                    else:
                        print (f"NO MATCH BOOLEAN:{table} and {created_field}")


            print(f"Intersect Count Adding completed for {duplicated_layer}.")
            conn.commit()


        
        except Exception as e:
                conn.rollback() 
                print(f"Ein Fehler ist aufgetreten: {e}")
