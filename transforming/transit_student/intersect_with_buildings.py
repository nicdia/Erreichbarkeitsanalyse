from sqlalchemy import text
import re
from collections import defaultdict

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
    """
    Aktualisiert die Geometriedaten in den Tabellen eines Schemas direkt auf SRID 25832,
    anstatt eine neue Tabelle zu erstellen.
    """
    source_schema = intersect_settings[0]["source_schema"]

    with db_con.connect() as conn:
        try:
            # Alle Tabellen im angegebenen Schema abrufen
            tables = conn.execute(text(f"""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = :schema
            """), {"schema": source_schema}).fetchall()
            
            for table in tables:
                table_name = table[0]
                print(f"Prüfe Tabelle: {table_name}")

                # Geometriespalte ermitteln
                isochrone_geom_col = get_geometry_column(conn, source_schema, table_name)
                if not isochrone_geom_col:
                    print(f"Überspringe Tabelle {table_name}, da keine Geometriespalte gefunden wurde.")
                    continue

                print(f"Transformiere Geometriespalte '{isochrone_geom_col}' in Tabelle '{table_name}' auf SRID 25832.")
                
                # Geometriespalte direkt per ALTER TABLE ändern
                conn.execute(text(f"""
                    ALTER TABLE {source_schema}.{table_name}
                    ALTER COLUMN {isochrone_geom_col}
                    TYPE geometry(Geometry, 25832)
                    USING ST_Transform({isochrone_geom_col}, 25832);
                """))
                conn.commit()

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
                intersect_table = f"{target_schema}.{table_name}_{keyword}"
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

def does_boolean_field_match_table(boolean_field, table):
    """
    Checks whether a boolean field name like "walk_4_63km_11111111_kinderaerzte"
    matches a table name like "walk_iso_4_63km_kinderaerzte_11111111".

    Conditions:
    1. The first segment (e.g., "walk") must match.
    2. The speed segment (e.g., "4_63km") must match.
    3. The last numeric segment (e.g., "11111111") must match.
    4. The indicator (e.g., "kinderaerzte") must match.
    5. The "iso" part in the table name is ignored.

    Returns:
        True if all conditions are met, otherwise False.
    """

    table_parts = table.split("_")
    boolean_parts = boolean_field.split("_")

    # Safety check to ensure both have enough segments
    if len(table_parts) < 5 or len(boolean_parts) < 5:
        return False

    # Extract mode (walk, bicycle, transit, etc.)
    mode_table = table_parts[0]
    mode_boolean = boolean_parts[0]

    # Extract speed segment (e.g., "4_63km")
    speed_table = f"{table_parts[2]}_{table_parts[3]}"  # In table, it's after "iso"
    speed_boolean = f"{boolean_parts[1]}_{boolean_parts[2]}"  # In boolean field, it's earlier

    # Extract numeric identifier at the end (e.g., "11111111")
    numeric_table = table_parts[-1]
    numeric_boolean = boolean_parts[3]

    # Extract indicator (e.g., "kinderaerzte")
    indicator_table = table_parts[4]
    indicator_boolean = boolean_parts[4]

    # Compare all relevant parts
    return (
        mode_table == mode_boolean and
        speed_table == speed_boolean and
        numeric_table == numeric_boolean and
        indicator_table == indicator_boolean
    )
   
def does_aggregated_field_match_table(created_field, table):
    """
    Checks whether a table name like "walk_iso_4_63km_kinderaerzte_11111111"
    matches a field name like "walk_4_63km_11111111" according to the following rules:

    1. The first segment (e.g., "walk") must match.
    2. The speed segment (e.g., "4_63km") must match.
       In the table name, those parts are usually at indices [2] and [3], 
       while in the field name they are at indices [1] and [2].
    3. The last segment (e.g., "11111111") must match.
    4. Any additional parts in the table name (like "iso", "kinderzahnaerzte", etc.) are ignored.

    Returns:
        True if all conditions are met, otherwise False.
    """
    table_parts = table.split("_")
    field_parts = created_field.split("_")

    # We expect at least 4 parts in each to reliably extract mode, speed, and last segment
    if len(field_parts) < 4 or len(table_parts) < 4:
        return False

    # 1) The first segment must match (e.g., "walk")
    if table_parts[0] != field_parts[0]:
        return False

    # 2) The speed segment must match
    #    For the table name, it's at indices [2] and [3]: "4" and "63km"
    #    For the field name, it's at [1] and [2]: "4" and "63km"
    speed_table = f"{table_parts[2]}_{table_parts[3]}"
    speed_field = f"{field_parts[1]}_{field_parts[2]}"
    if speed_table != speed_field:
        return False

    # 3) The last segment (e.g., "11111111") must match
    if table_parts[-1] != field_parts[-1]:
        return False

    return True

    
def extract_aggregated_and_boolean_names(table_name, keyword):
    """
    Erwartet z.B. "walk_iso_4_63km_kinderzahnaerzte_1111111"

    Gibt zurück:
      aggregated_name = "walk_4_63km"
      boolean_name    = "walk_4_63km_kinderzahnaerzte"
    """

    parts = table_name.split("_")
    # Beispiel: ["walk", "iso", "4", "63km", "kinderzahnaerzte", "1111111"]

    if len(parts) < 5:
        # Falls das Format nicht stimmt, brechen wir mit Default-Werten ab.
        return table_name, table_name

    # Mode (walk, bicycle, transit, ...)
    mode = parts[0]

    # Speed + km => z.B. "4_63km"
    speed = f"{parts[2]}_{parts[3]}"

    # Indikator soll das vorletzte (oder das fünfte) Element sein
    # In vielen Fällen ist das parts[4], wenn parts[5] eine rein numerische ID ist.
    # Hier kannst du entscheiden, ob du die letzte Komponente prüfst:
    # Wir nehmen standardmäßig parts[4] als Indikator
    indicator = parts[4]
    # Falls du ALLE Teile außer dem letzten "1111111" möchtest:
    # indicator = "_".join(parts[4:-1])

    # Aggregated-Feld => "walk_4_63km"
    aggregated_name = f"{mode}_{speed}_{keyword}"

    # Boolean-Feld => z.B. "walk_4_63km_kinderzahnaerzte"
    boolean_name = f"{aggregated_name}_{indicator}"

    return aggregated_name, boolean_name


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
                aggregated_field_name, boolean_field_name = extract_aggregated_and_boolean_names(table_name=table, keyword = keyword)
                
                if aggregated_field_name not in created_aggregated_fields:
                    create_intersect_counting_field(duplicated_building_layer=duplicated_layer,db_con=conn, new_aggregated_field_name=aggregated_field_name)
                    created_aggregated_fields.append(aggregated_field_name)
                create_indicator_boolean_fields(duplicated_building_layer=duplicated_layer, db_con=conn,field_name = boolean_field_name)
                created_boolean_fields.append(boolean_field_name)
            print (f"this is all created aggregated fields: {created_aggregated_fields}")
            print (f"this is all created boolean fields: {created_boolean_fields}")
            for table in tables:
                for created_field in created_aggregated_fields:
                    if does_aggregated_field_match_table(created_field, table):
                        print (f"MATCH AGGREGATED: {table} count will be added in field {created_field}")
                        score_factor = extract_increment_factor(table, score_system)
                        add_intersect_feature_count(schema_name=intersect_results_schema,table_name = table, wohngebaeude_table=duplicated_layer, field_name=created_field, db_con=conn, score_factor=score_factor)
                    else:
                        print (f"NO MATCH AGGREGATED:{table} and {created_field}")
                for created_field in created_boolean_fields:
                    if does_boolean_field_match_table(boolean_field = created_field, table = table):
                        print (f"MATCH BOOLEAN: {table} boolean will be added in field {created_field}")
                        add_intersect_boolean_values(schema_name=intersect_results_schema,table_name = table, wohngebaeude_table=duplicated_layer, field_name=created_field, db_con=conn)
                    else:
                        print (f"NO MATCH BOOLEAN:{table} and {created_field}")


            print(f"Intersect Count Adding completed for {duplicated_layer}.")
            conn.commit()


        
        except Exception as e:
                conn.rollback() 
                print(f"Ein Fehler ist aufgetreten: {e}")


# import re
# from collections import defaultdict

# def execute_intersect_count_adding(intersect_settings, db_con, prefix_new_table):
#     """
#     Diese Funktion fügt Zähl- und Boolean-Informationen zu einem duplizierten Wohngebäudelayer hinzu,
#     basierend auf den Intersection-Ergebnissen in mehreren Tabellen. 
#     Neu: Pro 'Geschwindigkeit' (walk_iso_3, walk_iso_4, etc.) werden nur zwei Tabellen berücksichtigt.
#     """

#     intersect_results_schema = intersect_settings["target_schema"]
#     original_wohngebaeude_table = intersect_settings["wohngebaeude_table"]
#     wohngebaeude_schema, wohngebaeude_table_name = original_wohngebaeude_table.split(".")
#     score_system = intersect_settings["score_system"]
#     keyword = intersect_settings["keyword"]

#     with db_con.connect() as conn:
#         try:
#             # 1) Gebäude-Layer duplizieren
#             duplicated_layer = duplicate_building_layer(
#                 conn, 
#                 prefix_new_table, 
#                 wohngebaeude_schema, 
#                 original_wohngebaeude_table, 
#                 wohngebaeude_table_name
#             )

#             # 2) Alle (Intersection-)Tabellen holen
#             all_tables = get_tables(schema=intersect_results_schema, db_con=conn)
#             print(f"Alle gefundenen Tabellen: {all_tables}")

#             # 3) Gruppierung nach 'walk_iso_X' durchführen,
#             #    damit man pro 'Geschwindigkeit' nur zwei Tabellen nimmt.
#             grouped_tables = defaultdict(list)
#             for table in all_tables:
#                 # Muster: walk_iso_3_52km_xy... -> Gruppe = walk_iso_3
#                 match = re.match(r"^(walk_iso_\d+)_", table)
#                 if match:
#                     group_key = match.group(1)  # z.B. "walk_iso_3"
#                 else:
#                     # Falls das Pattern bei manchen Tabellen nicht zutrifft, als eigene Gruppe behandeln
#                     group_key = table
#                 grouped_tables[group_key].append(table)

#             # 4) Pro Gruppe (z.B. walk_iso_3) nur die ersten zwei Tabellen heraussuchen
#             filtered_tables = []
#             for group_key, tables_in_group in grouped_tables.items():
#                 filtered_tables.extend(tables_in_group[:2])  # nur die ersten zwei

#             print(f"Wir nutzen nur diese Tabellen weiter (max. 2 pro Geschwindigkeit): {filtered_tables}")

#             # 5) Felder anlegen (Zählfelder, Boolean-Felder) auf dem duplizierten Layer
#             created_aggregated_fields = []
#             created_boolean_fields = []

#             for table in filtered_tables:

#                 # Aggregiertes Feld
#                 aggregated_field_name, boolean_field_name = extract_aggregated_and_boolean_names(table_name=table)

#                 if aggregated_field_name not in created_aggregated_fields:
#                     create_intersect_counting_field(
#                         duplicated_building_layer=duplicated_layer,
#                         db_con=conn,
#                         new_aggregated_field_name=aggregated_field_name
#                     )
#                     created_aggregated_fields.append(aggregated_field_name)


#                 create_indicator_boolean_fields(
#                     duplicated_building_layer=duplicated_layer,
#                     db_con=conn,
#                     field_name=boolean_field_name
#                 )
#                 created_boolean_fields.append(boolean_field_name)

#             print(f"Erzeugte Zählfelder: {created_aggregated_fields}")
#             print(f"Erzeugte Boolean-Felder: {created_boolean_fields}")

#             # 6) Zählwerte und Boolean-Werte hinzufügen
#             for table in filtered_tables:
#                 for created_field in created_aggregated_fields:
#                     if does_field_match_table(created_field, table):
#                         print(f"MATCH AGGREGATED: {table} -> Zählen in Feld {created_field}")
#                         score_factor = extract_increment_factor(table, score_system)
#                         add_intersect_feature_count(
#                             schema_name=intersect_results_schema,
#                             table_name=table,
#                             wohngebaeude_table=duplicated_layer,
#                             field_name=created_field,
#                             db_con=conn,
#                             score_factor=score_factor
#                         )
#                     else:
#                         print(f"NO MATCH AGGREGATED: {table} and {created_field}")

#                 for created_field in created_boolean_fields:
#                     if created_field in table:
#                         print(f"MATCH BOOLEAN: {table} -> Boolean in Feld {created_field}")
#                         add_intersect_boolean_values(
#                             schema_name=intersect_results_schema,
#                             table_name=table,
#                             wohngebaeude_table=duplicated_layer,
#                             field_name=created_field,
#                             db_con=conn
#                         )
#                     else:
#                         print(f"NO MATCH BOOLEAN: {table} and {created_field}")

#             print(f"Intersect Count Adding abgeschlossen für {duplicated_layer}.")
#             conn.commit()

#         except Exception as e:
#             conn.rollback()
#             print(f"Ein Fehler ist aufgetreten: {e}")
