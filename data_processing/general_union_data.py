from sqlalchemy import inspect
from sqlalchemy.exc import SQLAlchemyError

def handle_conf_union(db_con, union_config):
    print ("this is union_config")
    with db_con.connect() as connection:
        inspector = inspect(db_con)
        schemas = inspector.get_schema_names()
        print(f"Schemas found: {schemas}")
        union_schemas = [
            schema for schema in schemas 
            if schema not in union_config 
            and "_original" not in schema 
            and "_not_attr_filtered" not in schema
        ]
        return union_schemas

def union_ops(db_con, union_schemas, geom_field):
    print (f"this is union schemas: {union_schemas}")
    with db_con.connect() as connection:
        inspector = inspect(db_con)
        for schema in union_schemas:
            tables = inspector.get_table_names(schema=schema)
            if not tables:
                print(f"No tables found in schema: {schema}")
                continue
            
            # Generate the union query
            select_expr = " UNION ALL ".join([f"SELECT {geom_field} FROM {schema}.{table}" for table in tables])
            complete_query = f"""
            SELECT ST_Union({geom_field}) AS unified_geometry 
            FROM (
                {select_expr}
            ) AS combined_geometries;
            """
            
            print(f"Executing query for schema {schema}:")
            print(complete_query)

            try:
                result = connection.execute(complete_query)
                for row in result:
                    print(row)
            except SQLAlchemyError as e:
                print(f"An error occurred while executing the query for schema {schema}: {e}")