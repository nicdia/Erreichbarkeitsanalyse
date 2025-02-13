from general_attribute_filtering import filter_and_create_table, handle_conf_attrfilter, custom_ALKIS_building_filtering
from general_union_data import union_tables, handle_conf_union
from kids_specific_ops import custom_elementary_sports_halls 
from intersect_with_buildings import intersect_buildings_isochrones, handle_conf_intersect, execute_intersect_count_adding, transform_otp_fetch_to_25832

from util_fcts import connect2DB
import json



def main_processing():
    # set up
    with open("C:\\Master\\GeoinfoPrj_Sem1\\Erreichbarkeitsanalyse\\data_processing_db_ops\\config_data_processing.json", "r") as file:
            config = json.load(file)


    db_con = connect2DB()
    geom_field_name = config["table_processing"]["geom_field"]
    ############## get the configs#################
    attr_filter_config = handle_conf_attrfilter(config)
    union_config = handle_conf_union(config)
    intersect_config = handle_conf_intersect(config)
###################################################

    # if attr_filter_config:
    #     filter_and_create_table(attr_filter_config, db_con)
    #     #custom_ALKIS_building_filtering(db_con)
    #     #custom_elementary_sports_halls(db_con)

    # if union_config:
    #       union_tables(db_con, union_config)
    
    if intersect_config:
        #transform_otp_fetch_to_25832(intersect_settings= intersect_config, db_con=db_con)
        for run in intersect_config:
            print (f"this is run: {run}")
            intersect_buildings_isochrones( run, db_con)
            execute_intersect_count_adding (run, db_con, "10Feb")




main_processing()

