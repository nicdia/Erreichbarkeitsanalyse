--- query to get the avg and the median of which score was achieved per modus students
SELECT * FROM (
    SELECT 'Bicycle 11.02kmh' AS Modus,
           ROUND(AVG(bicycle_3_06km_11111111)) AS Durchschnitt,
           PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY bicycle_3_06km_11111111) AS Median,
           'Bicycle' AS Modus_Sortierung,
           11.02 AS Geschwindigkeit
    FROM flurstuecke.students_wohngebaeude

    UNION ALL

    SELECT 'Bicycle 15.08kmh',
           ROUND(AVG(bicycle_4_19km_11111111)),
           PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY bicycle_4_19km_11111111),
           'Bicycle',
           15.08
    FROM flurstuecke.students_wohngebaeude

    UNION ALL

    SELECT 'Bicycle 20.99kmh',
           ROUND(AVG(bicycle_5_83km_11111111)),
           PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY bicycle_5_83km_11111111),
           'Bicycle',
           20.99
    FROM flurstuecke.students_wohngebaeude

    UNION ALL

    SELECT 'Transit 3.89kmh',
           ROUND(AVG(transitwalk_1_08km_11111111)),
           PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY transitwalk_1_08km_11111111),
           'Transit',
           3.89
    FROM flurstuecke.students_wohngebaeude

    UNION ALL

    SELECT 'Transit 5.22kmh',
           ROUND(AVG(transitwalk_1_45km_11111111)),
           PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY transitwalk_1_45km_11111111),
           'Transit',
           5.22
    FROM flurstuecke.students_wohngebaeude

    UNION ALL

    SELECT 'Transit 6.84kmh',
           ROUND(AVG(transitwalk_1_9km_11111111)),
           PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY transitwalk_1_9km_11111111),
           'Transit',
           6.84
    FROM flurstuecke.students_wohngebaeude

    UNION ALL

    SELECT 'Walk 3.89kmh',
           ROUND(AVG(walk_1_08km_11111111)),
           PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY walk_1_08km_11111111),
           'Walk',
           3.89
    FROM flurstuecke.students_wohngebaeude

    UNION ALL

    SELECT 'Walk 5.22kmh',
           ROUND(AVG(walk_1_45km_11111111)),
           PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY walk_1_45km_11111111),
           'Walk',
           5.22
    FROM flurstuecke.students_wohngebaeude

    UNION ALL

    SELECT 'Walk 6.84kmh',
           ROUND(AVG(walk_1_9km_11111111)),
           PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY walk_1_9km_11111111),
           'Walk',
           6.84
    FROM flurstuecke.students_wohngebaeude
) AS subquery

ORDER BY 
    CASE 
        WHEN Modus_Sortierung = 'Walk' THEN 1 
        WHEN Modus_Sortierung = 'Transit' THEN 2 
        WHEN Modus_Sortierung = 'Bicycle' THEN 3 
    END,
    Geschwindigkeit ASC;
	
	
-- avg + median for kids 
SELECT * FROM (
    SELECT 'Kind - Fahrrad 9kmh' AS Modus,
           ROUND(AVG(bicycle_2_5km_11111111)) AS Durchschnitt,
           PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY bicycle_2_5km_11111111) AS Median,
           'Bicycle' AS Modus_Sortierung,
           9 AS Geschwindigkeit
    FROM flurstuecke.kids_wohngebaeude

    UNION ALL

    SELECT 'Kind - Fahrrad 10kmh',
           ROUND(AVG(bicycle_2_78km_11111111)),
           PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY bicycle_2_78km_11111111),
           'Bicycle',
           10
    FROM flurstuecke.kids_wohngebaeude

    UNION ALL

    SELECT 'Kind - Fahrrad 11kmh',
           ROUND(AVG(bicycle_3_06km_11111111)),
           PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY bicycle_3_06km_11111111),
           'Bicycle',
           11
    FROM flurstuecke.kids_wohngebaeude

    UNION ALL

    SELECT 'Kind - OPNV 3.53kmh',
           ROUND(AVG(transitwalk_0_98km_11111111)),
           PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY transitwalk_0_98km_11111111),
           'Transit',
           3.53
    FROM flurstuecke.kids_wohngebaeude

    UNION ALL

    SELECT 'Kind - OPNV 4.64kmh',
           ROUND(AVG(transitwalk_1_29km_11111111)),
           PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY transitwalk_1_29km_11111111),
           'Transit',
           4.64
    FROM flurstuecke.kids_wohngebaeude

    UNION ALL

    SELECT 'Kind - OPNV 5.98kmh',
           ROUND(AVG(transitwalk_1_66km_11111111)),
           PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY transitwalk_1_66km_11111111),
           'Transit',
           5.98
    FROM flurstuecke.kids_wohngebaeude

    UNION ALL

    SELECT 'Kind - Gehen 3.53kmh',
           ROUND(AVG(walk_0_98km_11111111)),
           PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY walk_0_98km_11111111),
           'Walk',
           3.53
    FROM flurstuecke.kids_wohngebaeude

    UNION ALL

    SELECT 'Kind - Gehen 4.64kmh',
           ROUND(AVG(walk_1_29km_11111111)),
           PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY walk_1_29km_11111111),
           'Walk',
           4.64
    FROM flurstuecke.kids_wohngebaeude

    UNION ALL

    SELECT 'Kind - Gehen 5.98kmh',
           ROUND(AVG(walk_1_66km_11111111)),
           PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY walk_1_66km_11111111),
           'Walk',
           5.98
    FROM flurstuecke.kids_wohngebaeude
) AS subquery

ORDER BY 
    CASE 
        WHEN Modus_Sortierung = 'Walk' THEN 1 
        WHEN Modus_Sortierung = 'Transit' THEN 2 
        WHEN Modus_Sortierung = 'Bicycle' THEN 3 
    END,
    Geschwindigkeit ASC;

-- pretty sum up table for the main velocities 
SELECT * FROM (
    -- Fahrrad (Mittelgeschwindigkeiten)
    SELECT 'Fahrrad - 10kmh (Kinder)' AS Modus,
           ROUND(AVG(bicycle_2_78km_11111111)) AS Durchschnitt,
           PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY bicycle_2_78km_11111111) AS Median,
           'Bicycle' AS Modus_Sortierung,
           10 AS Geschwindigkeit
    FROM flurstuecke.kids_wohngebaeude

    UNION ALL

    SELECT 'Fahrrad - 15.08kmh (Studenten)',
           ROUND(AVG(bicycle_4_19km_11111111)),
           PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY bicycle_4_19km_11111111),
           'Bicycle',
           15.08
    FROM flurstuecke.students_wohngebaeude

    -- ÖPNV (Mittelgeschwindigkeiten)
    UNION ALL

    SELECT 'ÖPNV - 4.64kmh (Kinder)',
           ROUND(AVG(transitwalk_1_29km_11111111)),
           PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY transitwalk_1_29km_11111111),
           'Transit',
           4.64
    FROM flurstuecke.kids_wohngebaeude

    UNION ALL

    SELECT 'ÖPNV - 5.22kmh (Studenten)',
           ROUND(AVG(transitwalk_1_45km_11111111)),
           PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY transitwalk_1_45km_11111111),
           'Transit',
           5.22
    FROM flurstuecke.students_wohngebaeude

    -- Gehen (Mittelgeschwindigkeiten)
    UNION ALL

    SELECT 'Gehen - 4.64kmh (Kinder)',
           ROUND(AVG(walk_1_29km_11111111)),
           PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY walk_1_29km_11111111),
           'Walk',
           4.64
    FROM flurstuecke.kids_wohngebaeude

    UNION ALL

    SELECT 'Gehen - 5.22kmh (Studenten)',
           ROUND(AVG(walk_1_45km_11111111)),
           PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY walk_1_45km_11111111),
           'Walk',
           5.22
    FROM flurstuecke.students_wohngebaeude
) AS subquery

ORDER BY 
    CASE 
        WHEN Modus_Sortierung = 'Walk' THEN 1 
        WHEN Modus_Sortierung = 'Transit' THEN 2 
        WHEN Modus_Sortierung = 'Bicycle' THEN 3 
    END,
    Geschwindigkeit ASC;

