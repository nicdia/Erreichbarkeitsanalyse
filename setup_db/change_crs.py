from util_fcts import connect2DB, get_logging
from sqlalchemy import  text



#############################################################
def create_queries (geom_field, data):
    """
    Generates a list of SQL queries to alter and transform the coordinate reference system (CRS)
    of a geometry column in multiple tables.

    Parameters:
    geom_field (str): The name of the geometry field to be altered and transformed.
    data (list of dict): A list of dictionaries, each containing 'schema' and 'name' keys that 
                         specify the schema and table name respectively.

    Returns:
    list of tuple: A list of tuples, each containing a table name and two SQL query strings.
                   The first query alters the type of the geometry column to a specific CRS,
                   and the second query transforms the geometry data to that CRS.
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
    Executes a list of SQL queries to alter and transform the coordinate reference system (CRS)
    of a geometry column in multiple tables.

    Parameters:
    engine (sqlalchemy.engine.Engine): A SQLAlchemy engine object.
    queries (list of tuple): A list of tuples, each containing a table name and two SQL query strings.
                             The first query alters the type of the geometry column to a specific CRS,
                             and the second query transforms the geometry data to that CRS.

    Returns:
    None

    Raises:
    Exception: If any of the queries fail to execute.
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
    """
    Main function to change the coordinate reference system (CRS) of a geometry column in multiple tables.

    Parameters:
    geojson2localdb_data (list of dict): A list of dictionaries containing schema and table information.
    config (dict): A configuration dictionary containing the geom_field key with the name of the geometry column.

    Returns:
    None

    Raises:
    Exception: If any of the queries fail to execute.
    """
    try:
        db_con= connect2DB()
        queries = create_queries(geom_field=config["change_crs"]["geom_field"], data=geojson2localdb_data)
        execute_queries(db_con, queries)
    except Exception as error:
        print("Error in change_crs:", error)
