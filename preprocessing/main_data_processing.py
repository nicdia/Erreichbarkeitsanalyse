from general_attribute_filtering import filter_and_create_table, handle_conf_attrfilter, custom_ALKIS_building_filtering
from general_union_data import union_tables, handle_conf_union
from kids_specific_ops import custom_elementary_sports_halls 

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
###################################################

    if attr_filter_config:
        filter_and_create_table(attr_filter_config, db_con)
        #custom_ALKIS_building_filtering(db_con)
        #custom_elementary_sports_halls(db_con)

    if union_config:
          union_tables(db_con, union_config)
    



main_processing()

