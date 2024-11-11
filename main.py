from change_crs import main_change_crs
from geojson2localDB import main_geojson2localdb


def main():
    try:
        crs_config = main_geojson2localdb()
        main_change_crs(crs_config)
    except Exception as error:
        print (error)


main()