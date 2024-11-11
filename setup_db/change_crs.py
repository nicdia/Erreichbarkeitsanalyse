from ..misc.util_fcts import connect2DB, get_config, get_logging
from sqlalchemy import engine, text



#############################################################
def create_queries (geom_field, data):
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


def execute_queries(engine, queries, logger):
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
                        logger.error(error_message)  # Log the error

                    try:
                        connection.execute(text(qry2))
                        print(f"UPDATE query executed successfully on {table_name}")
                    except Exception as e:
                        error_message = f"Failed to execute UPDATE on {table_name}: {e}"
                        print(error_message)
                        logger.error(error_message)  # Log the error

                print("All queries executed and changes committed.")
    except Exception as error:
        print(f"Transaction Error: {error}")
        logger.error(f"Transaction Error: {error}")


def main_change_crs(geojson2localdb_data):
    try:
        engine = connect2DB()  
        configJSON = get_config()
        logger = get_logging()  
        queries = create_queries(geom_field=configJSON["change_crs"]["geom_field"], data=geojson2localdb_data)
        execute_queries(engine, queries, logger)
    except Exception as error:
        print("Error in change_crs:", error)
        logger.error(f"Error in change_crs: {error}")