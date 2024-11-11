from sqlalchemy import create_engine, Table, text, select, union_all
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv
import os
import psycopg2
from ..misc.util_fcts import setup, get_logging

def handle_config_settings(config):




def filter_and_create_table_sqlalchemy(schema, table, attribute, value, new_table_name, db_con):    
    try:
        query = f"""
        CREATE TABLE {schema}.{new_table_name} AS
        SELECT * FROM {schema}.{table}
        WHERE {attribute} = :value
        """

        with db_con.connect() as conn:
            conn.execute(text(query), {"value": value})
            conn.commit()
        
        print(f"Neue Tabelle '{new_table_name}' wurde erfolgreich erstellt.")
    
    except SQLAlchemyError as e:
        print(f"Ein Fehler ist aufgetreten: {e}")

def union_tables_and_create_table(schema, table_names, new_table_name, db_con):
    try:
        with db_con.connect() as conn:
            union_queries = []
            for table_name in table_names:
                table = Table(table_name, autoload_with=db_con)
                query = select([table])
                union_queries.append(query)
            
            union_query = union_all(*union_queries)

            create_query = f"CREATE TABLE {schema}.{new_table_name} AS {union_query}"
            conn.execute(text(create_query))
            conn.commit()
            
            print(f"Neue Tabelle '{new_table_name}' mit zusammengeführten Daten wurde erfolgreich erstellt.")
    
    except SQLAlchemyError as e:
        print(f"Ein Fehler ist aufgetreten: {e}")

def main_attribute_filtering():
    db_con, config = setup("config_data_processing.json")
    data = handle_config_settings(config)
    logger = get_logging()
