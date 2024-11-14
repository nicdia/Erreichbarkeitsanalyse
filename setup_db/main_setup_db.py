
from util_fcts import connect2DB, get_logging
from change_crs import main_change_crs
from geojson2localDB import main_geojson2localdb
from field_modifications import add_column_based_on_table_name
import json

def main():
    db_con = connect2DB()
    logger = get_logging()
    with open("C:\\Master\\GeoinfoPrj_Sem1\\Erreichbarkeitsanalyse\\setup_db\\config_setup_db.json", "r") as file:
            config = json.load(file)

    try:
        print ("lets go")
        crs_config = main_geojson2localdb(db_con, config)
        main_change_crs(crs_config, config)
        add_column_based_on_table_name(db_con)
    except Exception as error:

        print (error)

main()