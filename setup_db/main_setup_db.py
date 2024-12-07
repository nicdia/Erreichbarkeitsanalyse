
from util_fcts import connect2DB
from change_crs import main_change_crs
from geojson2localDB import main_geojson2localdb
from field_modifications import add_column_based_on_table_name
import json

def main():
    """
    Main function to set up the database.

    This function establishes a connection to the database, reads configuration settings 
    from a JSON file, and performs a series of operations on the database. It imports 
    data from GeoJSON files into the database, changes the coordinate reference system 
    (CRS) for specified tables, and adds a new column to tables based on their names.

    Raises:
        Exception: If any error occurs during the execution of the database operations.
    """
    db_con = connect2DB()
    with open("C:\\Master\\GeoinfoPrj_Sem1\\Erreichbarkeitsanalyse\\setup_db\\config_setup_db.json", "r") as file:
            config = json.load(file)
    try:
        original_tables = main_geojson2localdb(db_con, config, "_original")
        main_change_crs(original_tables, config)
        to_be_modified_tables = main_geojson2localdb(db_con, config, "")
        main_change_crs(to_be_modified_tables, config)
        add_column_based_on_table_name(db_con)
    except Exception as error:
        print (error)

main()