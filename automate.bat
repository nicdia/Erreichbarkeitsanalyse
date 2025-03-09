@echo off
CALL C:\Master\GeoinfoPrj_Sem1\Erreichbarkeitsanalyse\venv\Scripts\activate.bat
python C:\Master\GeoinfoPrj_Sem1\Erreichbarkeitsanalyse\fetch_data\iso_otp_1_5.py
python C:\Master\GeoinfoPrj_Sem1\Erreichbarkeitsanalyse\data_processing_db_ops\main_data_processing.py
pause