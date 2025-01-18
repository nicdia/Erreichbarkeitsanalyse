import json

######################################
with open ("C:\\Master\\GeoinfoPrj_Sem1\\Erreichbarkeitsanalyse\\fetch_data\\fetch_data_config.json", "r") as file:
    config = json.load(file)
URL = config["fetch_otp"]["server_url"]
MODE = list(config["fetch_otp"]["calculation_params"]["mode"].keys()[0])
SPEED = list(config["fetch_otp"]["calculation_params"]["mode"].values()[0])
DATE = config["fetch_otp"]["calculation_params"]["date"]
TIME = config["fetch_otp"]["calculation_params"]["time"]
PRECISION = config["fetch_otp"]["calculation_params"]["precisionMeters"]
CUTOFF = config["fetch_otp"]["calculation_params"]["cutoffSec"]

#####################################
# 1. get the data --> extract the cors from database layers
def extract_cors():
    pass
    # get access to fertigepunktlayer schema
    # loop through each table
    # loop through each feature
    # create a dict and as key the table name and as value the list of coordinates

def fetch_otp_api():
    pass
    # input is the dict with the coordinates
    # for each value in the cor list make a request
    # save the response

def create_geojson_from_otp_result():
    pass
    # do what is needed to create a geojon 

def import_geojson_to_db():
    # just copy the code from the other script or import that function!
    pass

def get_otp_isos():
    pass



# only walk
# http://localhost:8080/otp/routers/current/isochrone?algorithm=accSampling&fromPlace=53.59860878,9.99349447&mode=BICYCLE&bikeSpeed=4.916667&date=2024-12-12&time=10:00:00&precisionMeters=10&cutoffSec=900

# walk transit
# http://localhost:8080/otp/routers/current/isochrone?algorithm=accSampling&fromPlace=53.61542249,10.04778259&mode=WALK,TRANSIT&walkSpeed=1.34112&date=2024-12-12&time=10:00:00&precisionMeters=10&cutoffSec=900

# bicycle
# http://localhost:8080/otp/routers/current/isochrone?algorithm=accSampling&fromPlace=53.59860878,9.99349447&mode=BICYCLE&bikeSpeed=4.916667&date=2024-12-12&time=10:00:00&precisionMeters=10&cutoffSec=900


