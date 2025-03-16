This project was developed as part of a master's thesis. The objective was to analyze accessibility for two target groups in the context of the "15-minute city" concept, considering eight essential indicators for these groups. Three different modes of transport were evaluated and compared: walking, cycling, and public transport.

This repository contains all the scripts used for the analysis. It is further divided into the functional sections of the workflow. All scripts utilize the SQL Alchemy library to interact with a locally running PostgreSQL database with the PostGIS extension. In general, the scripts dynamically construct queries for executing ELT and ETL processes.

All sections were developed to rely on a central config.json file, where all paths are specified. The scripts themselves only require the configuration file path to be set. Using relative paths would have been an alternative approach, which is a key learning for future projects.

SetupDB Folder:
config_setup_db.json --> adjust paths here
geojson2localDB.py --> specify paths, and files will be uploaded into tables + schemas
change_crs.py --> adjusts the CRS of tables within a schema
field_modifications.py --> adds a field to each table that contains either "meta" or "osm" in its name, with the corresponding field value
util_fcts.py --> creates a database connection and contains other helper functions
main_setup_db.py --> the main script to execute, connecting functions from the other scripts in this folder

Preprocessing:
general_attribute_filtering.py --> filters tables based on attribute values
general_union_data.py --> unions all provided tables
kids_specific_ops.py --> custom functions specifically for student-related data
util_fcts.py --> duplicate file due to lack of knowledge regarding "main" and "init" functionality at the time
fetchGoogleMapsAPI.py --> fetches Google Maps API data and includes several control and retrieval functions. Ensure API key security.
main_data_processing.py --> the main script to execute; adjust config_data_processing.json before running

Transforming:
bicycle_student, transit_student, walk_student --> contains scripts with individual configurations that compute isochrones for final point data and perform building intersection operations, resulting in the final student living building layer
fetch_bicycle, fetch_transit, fetch_walk --> same process as for students
fetchall_kids.bat, fetchall_students.bat --> executes all scripts sequentially

SQLQueries:
All queries executed on the two transformed living buildings tables.

Misc:
short_filename --> adjusts the names of GeoJSON files
unpackzip --> extracts zip files
util_fcts --> helper functions for setting up the environment, now included in each relevant parent directory

Considerations for future reuse:
--> Start the OTP server: java -Xmx8G -jar otp.jar --router current --graphs graphs --server
--> When creating a new database, remember to activate the PostGIS extension! Everything else is automated; just ensure the configurations are correct.
--> Always work with the "original name" of the tables! When data operations are performed, the "old version" is renamed accordingly, e.g., original, not_attr_filtered, etc.
--> union_data: the list includes all "original names" of schemas that should be excluded from union operations. Since \_original tables are automatically created beforehand, they are not considered in the union process.
