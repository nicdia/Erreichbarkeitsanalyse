from attribute_filtering import filter_and_create_table, handle_conf_attrfilter, custom_ALKIS_building_filtering
from not_used_anymore.join_with_alkis import handle_conf_join_with_alkis, join_POI_with_ALKIS, rename_fields_with_schema
from util_fcts import connect2DB
import json
import os



def main_processing():
    # set up
    with open("C:\\Master\\GeoinfoPrj_Sem1\\Erreichbarkeitsanalyse\\data_processing\\config_data_processing.json", "r") as file:
            config = json.load(file)
    db_con = connect2DB()

    
    # 1. filter by field values
    attr_filter = handle_conf_attrfilter(config)
    # if attr_filter:
    #     filter_and_create_table(attr_filter, db_con)
    #     custom_ALKIS_building_filtering(db_con)

    join_config = handle_conf_join_with_alkis(config)

    if join_config:
        # 2. rename fields so there will be no error when joining
        #rename_fields_with_schema(db_con, join_config)
        #3. spatial join der POIs mit alkis daten
        join_POI_with_ALKIS(db_con, join_config) 

    #3. data source mismatch handling (delete osm features)

    #4. if multiple datasets, union them 

    # 5. create centroids in every polygon

    # --> result: one dataset for every schema, with only polygons that match flurstuecke/gebauede


main_processing()

