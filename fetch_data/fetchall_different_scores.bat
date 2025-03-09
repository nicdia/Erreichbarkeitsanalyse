@echo off
CALL C:\Master\GeoinfoPrj_Sem1\Erreichbarkeitsanalyse\venv\Scripts\activate.bat

echo STARTING CHILDREN

echo Running Bicycle Processing... CHILDREN
python C:\Master\GeoinfoPrj_Sem1\Erreichbarkeitsanalyse\fetch_data\different_scores_kids_bicycle\main_data_processing.py

echo.
echo =========================================================
echo [✅] BICYCLE PROCESSING COMPLETED
echo =========================================================
echo.
echo.

echo Running Transit Processing... CHILDREN
python C:\Master\GeoinfoPrj_Sem1\Erreichbarkeitsanalyse\fetch_data\different_scores_kids_walk\main_data_processing.py
echo.
echo =========================================================
echo [✅] TRANSIT PROCESSING COMPLETED
echo =========================================================
echo.
echo.

echo Running Walk Processing... CHILDREN

python C:\Master\GeoinfoPrj_Sem1\Erreichbarkeitsanalyse\fetch_data\different_scores_kids_transit\main_data_processing.py
echo.
echo =========================================================
echo [✅] WALK PROCESSING COMPLETED
echo =========================================================
echo.
echo.


echo STARTING STUDENTS
pause
echo Running Bicycle Processing... STUDENTS
python C:\Master\GeoinfoPrj_Sem1\Erreichbarkeitsanalyse\fetch_data\different_scores_students_bicycle\main_data_processing.py

echo.
echo =========================================================
echo [✅] BICYCLE PROCESSING COMPLETED
echo =========================================================
echo.
echo.

echo Running Transit Processing... STUDENTS
python C:\Master\GeoinfoPrj_Sem1\Erreichbarkeitsanalyse\fetch_data\different_scores_students_walk\main_data_processing.py
echo.
echo =========================================================
echo [✅] TRANSIT PROCESSING COMPLETED
echo =========================================================
echo.
echo.

echo Running Walk Processing... STUDENTS
python C:\Master\GeoinfoPrj_Sem1\Erreichbarkeitsanalyse\fetch_data\different_scores_students_transit\main_data_processing.py
echo.
echo =========================================================
echo [✅] WALK PROCESSING COMPLETED
echo =========================================================
echo.
echo.
