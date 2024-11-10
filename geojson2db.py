import geopandas
import sqlalchemy
import psycopg2
import os
import geoalchemy2

##########################################################################################################
# these need to be configured
db_schema = "bezirksgrenzen_gemarkungen"
datasource = ""
data_location  = "C:\\Master\\GeoinfoPrj_Sem1\\Rohdaten\\alkis"
data_format = [".json", ".geojson"]
#############################################################################################################



# default values, do not change
DB_HOST = "sem1erreichbarkeitsanalyse.clgy8k22qvp0.eu-central-1.rds.amazonaws.com"
DB_NAME = "stadt15min"
DB_USER= "postgres"
DB_PASSWORD = "jochenschiewe"
DB_PORT = "5432"

# establish db connection
engine = sqlalchemy.create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

# access the geojsons
files_with_extension = os.listdir(data_location)
files = []
for file_with in files_with_extension:
    for file_ending in data_format:
        if file_with.endswith(file_ending):
            file_without = os.path.splitext(file_with)
            files.append(file_without[0])
#print (files)
# abs_paths = [os.path.abspath(os.path.join(os.path.dirname(file), os.pardir, os.pardir, origin_data_folder, file)) for file in files_with_extension]
abs_paths = [os.path.join(data_location, file) for file in files_with_extension]
#print (abs_paths)
tpl_list = []
file_count = 0
for file in files:
    tpl = (file, abs_paths[file_count])
    tpl_list.append(tpl)
    file_count += 1

file_and_abspath = { tpl[0] : tpl[1] for tpl in tpl_list }
print (file_and_abspath)


# convert geojson to geopandas frame
for file, abspath in file_and_abspath.items():
    gdf = geopandas.read_file(abspath)
    # import into db
    gdf.to_postgis(name= file + datasource, con= engine, schema = db_schema)
    print (f"the geojson with the name {file} was imported into the db.")

print ("Script finished.")

