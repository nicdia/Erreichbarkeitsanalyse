from attribute_filtering import filter_and_create_table, handle_conf_attrfilter
from union_data import handle_conf_union, union_tables_and_create_table
from ..misc.util_fcts import setup, get_logging



def main_attribute_filtering():
    db_con, config = setup("config_data_processing.json")
    logger = get_logging()
    attr_filter = handle_conf_attrfilter(config)
    if attr_filter:
        filter_and_create_table(attr_filter, db_con)
    union = handle_conf_union(config)

