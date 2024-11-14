from util_fcts import connect2DB, get_logging
from sqlalchemy import  text



#############################################################
def create_queries (geom_field, data):
    
    """
    Generates a list of SQL queries to change the coordinate reference system (CRS)
    of geometry columns in specified database tables.

    Parameters:
    geom_field (str): The name of the geometry column to be altered in the tables.
    data (list of dict): A list of configurations, where each configuration contains 
                         'schema' and 'name' keys representing the schema and table name.

    Returns:
    list of tuples: Each tuple contains the table name and two SQL queries. The first query 
                    alters the geometry column to set its SRID to 25832, and the second query 
                    transforms the geometry to the new CRS.
    """
    queries = []
    for config in data:
        schema = config.get("schema")
        table_name = config.get("name")
        query1 = f'''
    ALTER TABLE {schema}."{table_name}"
    ALTER COLUMN {geom_field} TYPE Geometry(Geometry, 25832)
    USING ST_SetSRID({geom_field}, 25832);
    '''
        query2 = f'''
    UPDATE {schema}."{table_name}"
    SET {geom_field} = ST_Transform({geom_field}, 25832);
    '''
        qry_tpl = (table_name, query1, query2)
        queries.append(qry_tpl)
    return queries


def execute_queries(engine, queries):
    """
    Executes a list of SQL queries to change the coordinate reference system (CRS)
    of geometry columns in specified database tables.

    Parameters:
    engine (sqlalchemy.engine.Engine): A SQLAlchemy engine object.
    queries (list of tuples): A list of tuples, where each tuple contains the table name and two SQL queries.
                              The first query alters the geometry column to set its SRID to 25832, and the second query
                              transforms the geometry to the new CRS.
    logger (logging.Logger): A logger object to log any errors that occur during query execution.

    Returns:
    None
    """
    try:
        with engine.connect() as connection:
            with connection.begin():  # Open a transaction block
                for table_name, qry1, qry2 in queries:
                    try:
                        connection.execute(text(qry1))
                        print(f"ALTER TABLE query executed successfully on {table_name}")
                    except Exception as e:
                        error_message = f"Failed to execute ALTER TABLE on {table_name}: {e}"
                        print(error_message)


                    try:
                        connection.execute(text(qry2))
                        print(f"UPDATE query executed successfully on {table_name}")
                    except Exception as e:
                        error_message = f"Failed to execute UPDATE on {table_name}: {e}"
                        print(error_message)


                print("All queries executed and changes committed.")
    except Exception as error:
        print(f"Transaction Error: {error}")



def main_change_crs(geojson2localdb_data, config):
    try:
        db_con= connect2DB()
        queries = create_queries(geom_field=config["change_crs"]["geom_field"], data=geojson2localdb_data)
        execute_queries(db_con, queries)
    except Exception as error:
        print("Error in change_crs:", error)
