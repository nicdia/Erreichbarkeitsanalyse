from util_fcts import connect2DB
from sqlalchemy import engine, text
import json

with open("config.json", "r") as file:
    config = json.load(file)
#############################################################
def create_queries (config):
    queries = []
    for schema, tables in config["change_crs"].items():
        for table_name, geom_field in tables.items():
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
    try:
        with engine.connect() as connection:
            with connection.begin():  # Transaktionsblock öffnen
                for table_name, qry1, qry2 in queries:
                    connection.execute(text(qry1))
                    print(f"ALTER TABLE query executed successfully on {table_name} ")
                    connection.execute(text(qry2))
                    print(f"UPDATE query executed on successfully {table_name}")
                print(f"All queries executed and changes committed in table {table_name}.")
    except Exception as error:
        print(f"Fehler: {error}")


def main_change_crs():
    try:
        engine = connect2DB()
        queries = create_queries(config)
        execute_queries(engine, queries )
    except Exception as error:
        print ("Error in change_crs:", error)


main_change_crs()