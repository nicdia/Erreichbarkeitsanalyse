from attribute_filtering import filter_and_create_table, handle_conf_attrfilter, custom_ALKIS_building_filtering

from union_data import union_ops, handle_conf_union
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
    union_config = handle_conf_union(db_con, config["table_processing"]["union_data"])
###################################################

    if attr_filter_config:
        filter_and_create_table(attr_filter_config, db_con)
        custom_ALKIS_building_filtering(db_con)
        custom_elementary_sports_halls(db_con)

    # if union_config:
    #       union_ops(db_con, union_config, geom_field_name)
          
    #3. data source mismatch handling (delete osm features)

    # --> result: one dataset for every schema, with only polygons that match flurstuecke/gebauede


main_processing()

