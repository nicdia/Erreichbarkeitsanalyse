from sqlalchemy import text, Table, select, union_all
from sqlalchemy.exc import SQLAlchemyError

def handle_conf_union(config):
    union_tables = config["union_data"]
    return union_tables

def union_tables_and_create_table(union_dict, db_con):
    try:
        with db_con.connect() as conn:
            for key, table_list in union_dict.items():
                union_queries = []
                
                for table_name in table_list:
                    table = Table(table_name,autoload_with=db_con)
                    query = select(table)  
                    union_queries.append(query)
            
                # UNION der Abfragen erstellen
                union_query = union_all(*union_queries)
                new_table_name = f"union_{key}"
                
                # CREATE TABLE Query als Text
                create_query = text(f"CREATE TABLE {key}.{new_table_name} AS {union_query}")
                conn.execute(create_query)
                conn.commit()
            
                print(f"Neue Tabelle '{new_table_name}' mit zusammengeführten Daten wurde erfolgreich erstellt.")
    
    except SQLAlchemyError as e:
        print(f"Ein Fehler ist aufgetreten: {e}")