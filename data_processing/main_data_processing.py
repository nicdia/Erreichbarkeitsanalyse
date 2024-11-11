from data_processing.attribute_filtering import filter_and_create_table, handle_conf_attrfilter
from data_processing.union_data import union_tables_and_create_table, create_union_table
from misc.util_fcts import setup, get_logging
import json
import os



def main_processing():
    config_path = os.path.join("data_processing", "config_data_processing.json")
    db_con, config = setup(config_path)
    logger = get_logging()
    # attr_filter = handle_conf_attrfilter(config)
    # if attr_filter:
    #     filter_and_create_table(attr_filter, db_con)


    config_path = os.path.join("setup_db", "config_setup_db.json")

    # Öffne und lade die JSON-Datei
    with open(config_path, "r") as file:
        config_db_setup = json.load(file)

    schemas = list(config_db_setup["geojson2localdb"]["data"].keys())
    create_union_table(db_con, schemas)


