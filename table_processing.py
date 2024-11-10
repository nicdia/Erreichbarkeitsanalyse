from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os
from util_fcts import connect2DB


db_con = connect2DB()
# 1. code for filtering by attributes
config = {
    "schools": {
        "staatliche_schulen_meta": {"field": "kapitelbezeichnung",
                                     "value": "Grundschulen"}
    },
}




# 2. dont know yet