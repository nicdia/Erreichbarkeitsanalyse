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