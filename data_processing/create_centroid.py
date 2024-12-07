from sqlalchemy import text

def handle_centroid_config(config):
    """
    Handles the configuration for creating centroids. The returned object has the structure of that the keys are the schema names and as value there is a list of the table names

    Args:
        config (dict): The configuration dictionary.

    Returns:
        dict: The configuration for creating centroids.
    """
    centroid_config = config["table_processing"]["create_centroids"]
    return centroid_config

def create_centroids(centroid_config, db_con):
    """
    Creates a new column named 'centroid' in the given table(s) of the given schema(s) if it does not already exist.
    The column is of type geometry(Point, 25832) and contains the centroid of the geometry in the given geom_col.
    If the geometry is not a polygon or multipolygon, the centroid is not calculated.

    Args:
        centroid_config (dict): The configuration dictionary for creating centroids. The keys are the schema names and as value there is a list of the table names.
        db_con (sqlalchemy.engine.Engine): The database connection.

    Returns:
        None
    """

        geom_col = centroid_config["geometry"]
        for schema, table_list in centroid_config.items():
            if schema != "geometry": 
                for table_name in table_list:
                    query_create_centroids = text(f"""
                    DO $$
                    BEGIN
                        IF NOT EXISTS (
                            SELECT 1 
                            FROM information_schema.columns 
                            WHERE table_schema = '{schema}' AND table_name = '{table_name}' AND column_name = 'centroid'
                        ) THEN
                            ALTER TABLE {schema}.{table_name} ADD COLUMN centroid geometry(Point, 25832);
                        END IF;
                    END $$;
                    """)
                    

                    query_calculate_centroids = text(f"""
                    UPDATE {schema}.{table_name}
                    SET centroid = ST_Centroid({geom_col})
                    WHERE {geom_col} IS NOT NULL AND ST_GeometryType({geom_col}) IN ('ST_Polygon', 'ST_MultiPolygon');
                    """)

                    with db_con.connect() as conn:
                        conn.execute(query_create_centroids)
                        conn.execute(query_calculate_centroids)
                        conn.commit()
                    print ("finish")

    # set up the query to be executed
    # try to execute the query