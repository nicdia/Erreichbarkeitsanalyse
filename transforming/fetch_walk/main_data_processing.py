
from intersect_with_buildings import intersect_buildings_isochrones, handle_conf_intersect, execute_intersect_count_adding, transform_otp_fetch_to_25832

from util_fcts import connect2DB
import json



def main_processing():
    # set up
    with open("C:\\Master\\GeoinfoPrj_Sem1\\Erreichbarkeitsanalyse\\fetch_data\\fetch_walk\\config_data_processing.json", "r") as file:
            config = json.load(file)


    db_con = connect2DB()
    geom_field_name = config["table_processing"]["geom_field"]
    ############## get the configs#################

    intersect_config = handle_conf_intersect(config)
###################################################


    if intersect_config:
        transform_otp_fetch_to_25832(intersect_settings= intersect_config, db_con=db_con)
        for run in intersect_config:
            print (f"this is run: {run}")
            intersect_buildings_isochrones( run, db_con)
            execute_intersect_count_adding (run, db_con, "kids")




main_processing()

