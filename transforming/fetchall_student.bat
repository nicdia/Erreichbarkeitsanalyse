@echo off
CALL C:\Master\GeoinfoPrj_Sem1\Erreichbarkeitsanalyse\venv\Scripts\activate.bat

echo Running Bicycle Processing...
python C:\Master\GeoinfoPrj_Sem1\Erreichbarkeitsanalyse\fetch_data\bicycle_student\iso_otp_1_5.py
python C:\Master\GeoinfoPrj_Sem1\Erreichbarkeitsanalyse\fetch_data\bicycle_student\main_data_processing.py
echo.
echo =========================================================
echo [✅] BICYCLE PROCESSING COMPLETED
echo =========================================================
echo.
echo.

echo Running Transit Processing...
python C:\Master\GeoinfoPrj_Sem1\Erreichbarkeitsanalyse\fetch_data\transit_student\iso_otp_1_5.py
python C:\Master\GeoinfoPrj_Sem1\Erreichbarkeitsanalyse\fetch_data\transit_student\main_data_processing.py
echo.
echo =========================================================
echo [✅] TRANSIT PROCESSING COMPLETED
echo =========================================================
echo.
echo.

echo Running Walk Processing...
python C:\Master\GeoinfoPrj_Sem1\Erreichbarkeitsanalyse\fetch_data\walk_student\iso_otp_1_5.py
python C:\Master\GeoinfoPrj_Sem1\Erreichbarkeitsanalyse\fetch_data\walk_student\main_data_processing.py
echo.
echo =========================================================
echo [✅] WALK PROCESSING COMPLETED
echo =========================================================
echo.
echo.

pause