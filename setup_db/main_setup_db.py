from setup_db.change_crs import main_change_crs
from setup_db.geojson2localDB import main_geojson2localdb
from setup_db.add_field import add_column_based_on_table_name
from misc.util_fcts import setup, get_logging

def main():
    db_con, config = setup("setup_db/config_setup_db.json")
    logger = get_logging()
    try:
        crs_config = main_geojson2localdb()
        main_change_crs(crs_config)
        add_column_based_on_table_name(db_con)
    except Exception as error:
        print (error)

