from general_attribute_filtering import filter_and_create_table, handle_conf_attrfilter, custom_ALKIS_building_filtering
from general_union_data import union_tables, handle_conf_union
from kids_specific_ops import custom_elementary_sports_halls 
from create_centroid import create_centroids, handle_centroid_config

from util_fcts import connect2DB
import json
import os



def main_processing():
    # set up
    with open("C:\\Master\\GeoinfoPrj_Sem1\\Erreichbarkeitsanalyse\\data_processing\\config_data_processing.json", "r") as file:
            config = json.load(file)


    db_con = connect2DB()
    geom_field_name = config["table_processing"]["geom_field"]
    ############## get the configs#################
    attr_filter_config = handle_conf_attrfilter(config)
    centroid_creation_config = handle_centroid_config(config)
    union_config = handle_conf_union(config)
###################################################

    if attr_filter_config:
        filter_and_create_table(attr_filter_config, db_con)
        custom_ALKIS_building_filtering(db_con)
        #custom_elementary_sports_halls(db_con)

    if union_config:
          union_tables(db_con, union_config)
    
    # if centroid_creation_config:
    #     create_centroids(centroid_creation_config, db_con)



    # --> result: one point dataset for every schema that can be passed into the analysis part


main_processing()

