
-------------------------------------- PREPARATION -----------------------------------
-- get the name of the geometry field, srid
SELECT f_geometry_column, srid
FROM geometry_columns 
WHERE f_table_schema = 'bezirksgrenzen_gemarkungen' 
AND f_table_name = 'bezirke';

SELECT f_geometry_column, srid 
FROM geometry_columns 
WHERE f_table_schema = 'flurstuecke' 
AND f_table_name = 'kids_wohngebaeude';

-- get names of cols
SELECT column_name
FROM information_schema.columns
WHERE table_name = 'kids_wohngebaeude';

SELECT column_name
FROM information_schema.columns
WHERE table_name = 'students_wohngebaeude';

-- create a view that appends a new field that declares for each feature the name of the bezirk/stadtviertel
CREATE MATERIALIZED VIEW flurstuecke.kids_32211222_wohngebaeude_mit_bezirk AS
SELECT 
    wg.*,  -- Alle Spalten aus der Wohngebäudetabelle
    bz.bezirk_name  -- Das neue Feld mit dem Namen des Bezirks
FROM 
    flurstuecke.kids_32211222_wohngebaeude wg
LEFT JOIN 
    bezirksgrenzen_gemarkungen.bezirke bz
ON 
    ST_Intersects(wg.geometry, bz.geometry);
	