import psycopg2



########################################################
# adjust these vars here
schema = "flurstuecke"
tables = [
    "flurstueck_alkis",
    "gebaeude_alkis"
]  
geom_field = "geometry"
#######################################################



#####################################################
DB_HOST = "sem1erreichbarkeitsanalyse.clgy8k22qvp0.eu-central-1.rds.amazonaws.com"
DB_NAME = "stadt15min"
DB_USER = "postgres"
DB_PASSWORD = "jochenschiewe"
DB_PORT = "5432"
#######################################################


########################################################################################################
queries = []
for table in tables:
    qry1 = f'''
    ALTER TABLE {schema}."{table}"
    ALTER COLUMN {geom_field} TYPE Geometry(Geometry, 25832)
    USING ST_SetSRID({geom_field}, 25832);
    '''
    qry2 = f'''
    UPDATE {schema}."{table}"
    SET {geom_field} = ST_Transform({geom_field}, 25832);
    '''
    qry_tpl = (qry1, qry2)
    queries.append(qry_tpl)


def establish_db_connection():
    try:
        connection = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT
        )
        cursor = connection.cursor()
        print("Connection established.")
        return connection, cursor
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Fehler: {error}")
        return None, None

def execute_queries(queries, cursor, connection):
    try:
        for qry in queries:
            cursor.execute(qry[0])
            print("ALTER TABLE query executed.")
            cursor.execute(qry[1])
            print("UPDATE query executed.")
        connection.commit()  # Änderungen speichern
        print("All queries executed and changes committed.")
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Fehler: {error}")
        connection.rollback()  # Rollback bei Fehlern
        print("Transaction rolled back.")

def main():
    connection, db_cursor = establish_db_connection()
    if db_cursor:
        execute_queries(queries=queries, cursor=db_cursor, connection=connection)
        db_cursor.close()
        connection.close()
        print("Connection closed.")

main()