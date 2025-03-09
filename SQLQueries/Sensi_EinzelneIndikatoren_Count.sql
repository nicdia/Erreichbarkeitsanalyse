
--------------------- FIRST STUDENTS -------------------------------
-- query, that lists the indicators hierarchically - how often is each indicator accessible 
    -- Universitäten
SELECT * FROM (
    SELECT 'Universität - Fahrrad 11.02kmh' AS Indikator, 
           SUM(CASE WHEN bicycle_3_06km_11111111_universitaet THEN 1 ELSE 0 END) AS Anzahl_Gebäude,
           'Fahrrad' AS Modus,
           11.02 AS Geschwindigkeit
    FROM flurstuecke.students_wohngebaeude

    UNION ALL

    SELECT 'Universität - Fahrrad 15.08kmh',
           SUM(CASE WHEN bicycle_4_19km_11111111_universitaet THEN 1 ELSE 0 END),
           'Fahrrad',
           15.08
    FROM flurstuecke.students_wohngebaeude

    UNION ALL

    SELECT 'Universität - Fahrrad 20.99kmh',
           SUM(CASE WHEN bicycle_5_83km_11111111_universitaet THEN 1 ELSE 0 END),
           'Fahrrad',
           20.99
    FROM flurstuecke.students_wohngebaeude

    UNION ALL

    SELECT 'Universität - OPNV 3.89kmh',
           SUM(CASE WHEN transitwalk_1_08km_11111111_universitaet THEN 1 ELSE 0 END),
           'ÖPNV',
           3.89
    FROM flurstuecke.students_wohngebaeude

    UNION ALL

    SELECT 'Universität - OPNV 5.22kmh',
           SUM(CASE WHEN transitwalk_1_45km_11111111_universitaet THEN 1 ELSE 0 END),
           'ÖPNV',
           5.22
    FROM flurstuecke.students_wohngebaeude

    UNION ALL

    SELECT 'Universität - OPNV 6.84kmh',
           SUM(CASE WHEN transitwalk_1_9km_11111111_universitaet THEN 1 ELSE 0 END),
           'ÖPNV',
           6.84
    FROM flurstuecke.students_wohngebaeude

    UNION ALL

    SELECT 'Universität - Gehen 3.89kmh',
           SUM(CASE WHEN walk_1_08km_11111111_universitaet THEN 1 ELSE 0 END),
           'Gehen',
           3.89
    FROM flurstuecke.students_wohngebaeude

    UNION ALL

    SELECT 'Universität - Gehen 5.22kmh',
           SUM(CASE WHEN walk_1_45km_11111111_universitaet THEN 1 ELSE 0 END),
           'Gehen',
           5.22
    FROM flurstuecke.students_wohngebaeude

    UNION ALL

    SELECT 'Universität - Gehen 6.84kmh',
           SUM(CASE WHEN walk_1_9km_11111111_universitaet THEN 1 ELSE 0 END),
           'Gehen',
           6.84
    FROM flurstuecke.students_wohngebaeude
) AS subquery

ORDER BY 
    CASE 
        WHEN Modus = 'Gehen' THEN 1 
        WHEN Modus = 'ÖPNV' THEN 2 
        WHEN Modus = 'Fahrrad' THEN 3 
    END,
    Geschwindigkeit ASC,
    Anzahl_Gebäude ASC;

	
    -- Parks
SELECT * FROM (
    SELECT 'Parks - Fahrrad 11.02kmh' AS Indikator, 
           SUM(CASE WHEN bicycle_3_06km_11111111_parks THEN 1 ELSE 0 END) AS Anzahl_Gebäude,
           'Fahrrad' AS Modus,
           11.02 AS Geschwindigkeit
    FROM flurstuecke.students_wohngebaeude

    UNION ALL

    SELECT 'Parks - Fahrrad 15.08kmh',
           SUM(CASE WHEN bicycle_4_19km_11111111_parks THEN 1 ELSE 0 END),
           'Fahrrad',
           15.08
    FROM flurstuecke.students_wohngebaeude

    UNION ALL

    SELECT 'Parks - Fahrrad 20.99kmh',
           SUM(CASE WHEN bicycle_5_83km_11111111_parks THEN 1 ELSE 0 END),
           'Fahrrad',
           20.99
    FROM flurstuecke.students_wohngebaeude

    UNION ALL

    SELECT 'Parks - OPNV 3.89kmh',
           SUM(CASE WHEN transitwalk_1_08km_11111111_parks THEN 1 ELSE 0 END),
           'ÖPNV',
           3.89
    FROM flurstuecke.students_wohngebaeude

    UNION ALL

    SELECT 'Parks - OPNV 5.22kmh',
           SUM(CASE WHEN transitwalk_1_45km_11111111_parks THEN 1 ELSE 0 END),
           'ÖPNV',
           5.22
    FROM flurstuecke.students_wohngebaeude

    UNION ALL

    SELECT 'Parks - OPNV 6.84kmh',
           SUM(CASE WHEN transitwalk_1_9km_11111111_parks THEN 1 ELSE 0 END),
           'ÖPNV',
           6.84
    FROM flurstuecke.students_wohngebaeude

    UNION ALL

    SELECT 'Parks - Gehen 3.89kmh',
           SUM(CASE WHEN walk_1_08km_11111111_parks THEN 1 ELSE 0 END),
           'Gehen',
           3.89
    FROM flurstuecke.students_wohngebaeude

    UNION ALL

    SELECT 'Parks - Gehen 5.22kmh',
           SUM(CASE WHEN walk_1_45km_11111111_parks THEN 1 ELSE 0 END),
           'Gehen',
           5.22
    FROM flurstuecke.students_wohngebaeude

    UNION ALL

    SELECT 'Parks - Gehen 6.84kmh',
           SUM(CASE WHEN walk_1_9km_11111111_parks THEN 1 ELSE 0 END),
           'Gehen',
           6.84
    FROM flurstuecke.students_wohngebaeude
) AS subquery

ORDER BY 
    CASE 
        WHEN Modus = 'Gehen' THEN 1 
        WHEN Modus = 'ÖPNV' THEN 2 
        WHEN Modus = 'Fahrrad' THEN 3 
    END,
    Geschwindigkeit ASC,
    Anzahl_Gebäude ASC;

    -- Bars
	SELECT * FROM (
    SELECT 'Bars - Fahrrad 11.02kmh' AS Indikator, 
           SUM(CASE WHEN bicycle_3_06km_11111111_bars THEN 1 ELSE 0 END) AS Anzahl_Gebäude,
           'Fahrrad' AS Modus,
           11.02 AS Geschwindigkeit
    FROM flurstuecke.students_wohngebaeude

    UNION ALL

    SELECT 'Bars - Fahrrad 15.08kmh',
           SUM(CASE WHEN bicycle_4_19km_11111111_bars THEN 1 ELSE 0 END),
           'Fahrrad',
           15.08
    FROM flurstuecke.students_wohngebaeude

    UNION ALL

    SELECT 'Bars - Fahrrad 20.99kmh',
           SUM(CASE WHEN bicycle_5_83km_11111111_bars THEN 1 ELSE 0 END),
           'Fahrrad',
           20.99
    FROM flurstuecke.students_wohngebaeude

    UNION ALL

    SELECT 'Bars - OPNV 3.89kmh',
           SUM(CASE WHEN transitwalk_1_08km_11111111_bars THEN 1 ELSE 0 END),
           'ÖPNV',
           3.89
    FROM flurstuecke.students_wohngebaeude

    UNION ALL

    SELECT 'Bars - OPNV 5.22kmh',
           SUM(CASE WHEN transitwalk_1_45km_11111111_bars THEN 1 ELSE 0 END),
           'ÖPNV',
           5.22
    FROM flurstuecke.students_wohngebaeude

    UNION ALL

    SELECT 'Bars - OPNV 6.84kmh',
           SUM(CASE WHEN transitwalk_1_9km_11111111_bars THEN 1 ELSE 0 END),
           'ÖPNV',
           6.84
    FROM flurstuecke.students_wohngebaeude

    UNION ALL

    SELECT 'Bars - Gehen 3.89kmh',
           SUM(CASE WHEN walk_1_08km_11111111_bars THEN 1 ELSE 0 END),
           'Gehen',
           3.89
    FROM flurstuecke.students_wohngebaeude

    UNION ALL

    SELECT 'Bars - Gehen 5.22kmh',
           SUM(CASE WHEN walk_1_45km_11111111_bars THEN 1 ELSE 0 END),
           'Gehen',
           5.22
    FROM flurstuecke.students_wohngebaeude

    UNION ALL

    SELECT 'Bars - Gehen 6.84kmh',
           SUM(CASE WHEN walk_1_9km_11111111_bars THEN 1 ELSE 0 END),
           'Gehen',
           6.84
    FROM flurstuecke.students_wohngebaeude
) AS subquery

ORDER BY 
    CASE 
        WHEN Modus = 'Gehen' THEN 1 
        WHEN Modus = 'ÖPNV' THEN 2 
        WHEN Modus = 'Fahrrad' THEN 3 
    END,
    Geschwindigkeit ASC,
    Anzahl_Gebäude ASC;

    -- Clubs
	SELECT * FROM (
    SELECT 'Clubs - Fahrrad 11.02kmh' AS Indikator, 
           SUM(CASE WHEN bicycle_3_06km_11111111_clubs THEN 1 ELSE 0 END) AS Anzahl_Gebäude,
           'Fahrrad' AS Modus,
           11.02 AS Geschwindigkeit
    FROM flurstuecke.students_wohngebaeude

    UNION ALL

    SELECT 'Clubs - Fahrrad 15.08kmh',
           SUM(CASE WHEN bicycle_4_19km_11111111_clubs THEN 1 ELSE 0 END),
           'Fahrrad',
           15.08
    FROM flurstuecke.students_wohngebaeude

    UNION ALL

    SELECT 'Clubs - Fahrrad 20.99kmh',
           SUM(CASE WHEN bicycle_5_83km_11111111_clubs THEN 1 ELSE 0 END),
           'Fahrrad',
           20.99
    FROM flurstuecke.students_wohngebaeude

    UNION ALL

    SELECT 'Clubs - OPNV 3.89kmh',
           SUM(CASE WHEN transitwalk_1_08km_11111111_clubs THEN 1 ELSE 0 END),
           'ÖPNV',
           3.89
    FROM flurstuecke.students_wohngebaeude

    UNION ALL

    SELECT 'Clubs - OPNV 5.22kmh',
           SUM(CASE WHEN transitwalk_1_45km_11111111_clubs THEN 1 ELSE 0 END),
           'ÖPNV',
           5.22
    FROM flurstuecke.students_wohngebaeude

    UNION ALL

    SELECT 'Clubs - OPNV 6.84kmh',
           SUM(CASE WHEN transitwalk_1_9km_11111111_clubs THEN 1 ELSE 0 END),
           'ÖPNV',
           6.84
    FROM flurstuecke.students_wohngebaeude

    UNION ALL

    SELECT 'Clubs - Gehen 3.89kmh',
           SUM(CASE WHEN walk_1_08km_11111111_clubs THEN 1 ELSE 0 END),
           'Gehen',
           3.89
    FROM flurstuecke.students_wohngebaeude

    UNION ALL

    SELECT 'Clubs - Gehen 5.22kmh',
           SUM(CASE WHEN walk_1_45km_11111111_clubs THEN 1 ELSE 0 END),
           'Gehen',
           5.22
    FROM flurstuecke.students_wohngebaeude

    UNION ALL

    SELECT 'Clubs - Gehen 6.84kmh',
           SUM(CASE WHEN walk_1_9km_11111111_clubs THEN 1 ELSE 0 END),
           'Gehen',
           6.84
    FROM flurstuecke.students_wohngebaeude
) AS subquery

ORDER BY 
    CASE 
        WHEN Modus = 'Gehen' THEN 1 
        WHEN Modus = 'ÖPNV' THEN 2 
        WHEN Modus = 'Fahrrad' THEN 3 
    END,
    Geschwindigkeit ASC,
    Anzahl_Gebäude ASC;


	-- Hausarzt
	SELECT * FROM (
    SELECT 'Hausärzte - Fahrrad 11.02kmh' AS Indikator, 
           SUM(CASE WHEN bicycle_3_06km_11111111_hausaerzte THEN 1 ELSE 0 END) AS Anzahl_Gebäude,
           'Fahrrad' AS Modus,
           11.02 AS Geschwindigkeit
    FROM flurstuecke.students_wohngebaeude

    UNION ALL

    SELECT 'Hausärzte - Fahrrad 15.08kmh',
           SUM(CASE WHEN bicycle_4_19km_11111111_hausaerzte THEN 1 ELSE 0 END),
           'Fahrrad',
           15.08
    FROM flurstuecke.students_wohngebaeude

    UNION ALL

    SELECT 'Hausärzte - Fahrrad 20.99kmh',
           SUM(CASE WHEN bicycle_5_83km_11111111_hausaerzte THEN 1 ELSE 0 END),
           'Fahrrad',
           20.99
    FROM flurstuecke.students_wohngebaeude

    UNION ALL

    SELECT 'Hausärzte - OPNV 3.89kmh',
           SUM(CASE WHEN transitwalk_1_08km_11111111_hausaerzte THEN 1 ELSE 0 END),
           'ÖPNV',
           3.89
    FROM flurstuecke.students_wohngebaeude

    UNION ALL

    SELECT 'Hausärzte - OPNV 5.22kmh',
           SUM(CASE WHEN transitwalk_1_45km_11111111_hausaerzte THEN 1 ELSE 0 END),
           'ÖPNV',
           5.22
    FROM flurstuecke.students_wohngebaeude

    UNION ALL

    SELECT 'Hausärzte - OPNV 6.84kmh',
           SUM(CASE WHEN transitwalk_1_9km_11111111_hausaerzte THEN 1 ELSE 0 END),
           'ÖPNV',
           6.84
    FROM flurstuecke.students_wohngebaeude

    UNION ALL

    SELECT 'Hausärzte - Gehen 3.89kmh',
           SUM(CASE WHEN walk_1_08km_11111111_hausaerzte THEN 1 ELSE 0 END),
           'Gehen',
           3.89
    FROM flurstuecke.students_wohngebaeude

    UNION ALL

    SELECT 'Hausärzte - Gehen 5.22kmh',
           SUM(CASE WHEN walk_1_45km_11111111_hausaerzte THEN 1 ELSE 0 END),
           'Gehen',
           5.22
    FROM flurstuecke.students_wohngebaeude

    UNION ALL

    SELECT 'Hausärzte - Gehen 6.84kmh',
           SUM(CASE WHEN walk_1_9km_11111111_hausaerzte THEN 1 ELSE 0 END),
           'Gehen',
           6.84
    FROM flurstuecke.students_wohngebaeude
) AS subquery

ORDER BY 
    CASE 
        WHEN Modus = 'Gehen' THEN 1 
        WHEN Modus = 'ÖPNV' THEN 2 
        WHEN Modus = 'Fahrrad' THEN 3 
    END,
    Geschwindigkeit ASC,
    Anzahl_Gebäude ASC;
	
	
	
	
	-- Zahnarzt
	SELECT * FROM (
    SELECT 'Zahnärzte - Fahrrad 11.02kmh' AS Indikator, 
           SUM(CASE WHEN bicycle_3_06km_11111111_zahnaerzte THEN 1 ELSE 0 END) AS Anzahl_Gebäude,
           'Fahrrad' AS Modus,
           11.02 AS Geschwindigkeit
    FROM flurstuecke.students_wohngebaeude

    UNION ALL

    SELECT 'Zahnärzte - Fahrrad 15.08kmh',
           SUM(CASE WHEN bicycle_4_19km_11111111_zahnaerzte THEN 1 ELSE 0 END),
           'Fahrrad',
           15.08
    FROM flurstuecke.students_wohngebaeude

    UNION ALL

    SELECT 'Zahnärzte - Fahrrad 20.99kmh',
           SUM(CASE WHEN bicycle_5_83km_11111111_zahnaerzte THEN 1 ELSE 0 END),
           'Fahrrad',
           20.99
    FROM flurstuecke.students_wohngebaeude

    UNION ALL

    SELECT 'Zahnärzte - OPNV 3.89kmh',
           SUM(CASE WHEN transitwalk_1_08km_11111111_zahnaerzte THEN 1 ELSE 0 END),
           'ÖPNV',
           3.89
    FROM flurstuecke.students_wohngebaeude

    UNION ALL

    SELECT 'Zahnärzte - OPNV 5.22kmh',
           SUM(CASE WHEN transitwalk_1_45km_11111111_zahnaerzte THEN 1 ELSE 0 END),
           'ÖPNV',
           5.22
    FROM flurstuecke.students_wohngebaeude

    UNION ALL

    SELECT 'Zahnärzte - OPNV 6.84kmh',
           SUM(CASE WHEN transitwalk_1_9km_11111111_zahnaerzte THEN 1 ELSE 0 END),
           'ÖPNV',
           6.84
    FROM flurstuecke.students_wohngebaeude

    UNION ALL

    SELECT 'Zahnärzte - Gehen 3.89kmh',
           SUM(CASE WHEN walk_1_08km_11111111_zahnaerzte THEN 1 ELSE 0 END),
           'Gehen',
           3.89
    FROM flurstuecke.students_wohngebaeude

    UNION ALL

    SELECT 'Zahnärzte - Gehen 5.22kmh',
           SUM(CASE WHEN walk_1_45km_11111111_zahnaerzte THEN 1 ELSE 0 END),
           'Gehen',
           5.22
    FROM flurstuecke.students_wohngebaeude

    UNION ALL

    SELECT 'Zahnärzte - Gehen 6.84kmh',
           SUM(CASE WHEN walk_1_9km_11111111_zahnaerzte THEN 1 ELSE 0 END),
           'Gehen',
           6.84
    FROM flurstuecke.students_wohngebaeude
) AS subquery

ORDER BY 
    CASE 
        WHEN Modus = 'Gehen' THEN 1 
        WHEN Modus = 'ÖPNV' THEN 2 
        WHEN Modus = 'Fahrrad' THEN 3 
    END,
    Geschwindigkeit ASC,
    Anzahl_Gebäude ASC;

	-- Lebensmitteleinkauf
	SELECT * FROM (
    SELECT 'Lebensmitteleinkauf - Fahrrad 11.02kmh' AS Indikator, 
           SUM(CASE WHEN bicycle_3_06km_11111111_lebensmitteleinkauf THEN 1 ELSE 0 END) AS Anzahl_Gebäude,
           'Fahrrad' AS Modus,
           11.02 AS Geschwindigkeit
    FROM flurstuecke.students_wohngebaeude

    UNION ALL

    SELECT 'Lebensmitteleinkauf - Fahrrad 15.08kmh',
           SUM(CASE WHEN bicycle_4_19km_11111111_lebensmitteleinkauf THEN 1 ELSE 0 END),
           'Fahrrad',
           15.08
    FROM flurstuecke.students_wohngebaeude

    UNION ALL

    SELECT 'Lebensmitteleinkauf - Fahrrad 20.99kmh',
           SUM(CASE WHEN bicycle_5_83km_11111111_lebensmitteleinkauf THEN 1 ELSE 0 END),
           'Fahrrad',
           20.99
    FROM flurstuecke.students_wohngebaeude

    UNION ALL

    SELECT 'Lebensmitteleinkauf - OPNV 3.89kmh',
           SUM(CASE WHEN transitwalk_1_08km_11111111_lebensmitteleinkauf THEN 1 ELSE 0 END),
           'ÖPNV',
           3.89
    FROM flurstuecke.students_wohngebaeude

    UNION ALL

    SELECT 'Lebensmitteleinkauf - OPNV 5.22kmh',
           SUM(CASE WHEN transitwalk_1_45km_11111111_lebensmitteleinkauf THEN 1 ELSE 0 END),
           'ÖPNV',
           5.22
    FROM flurstuecke.students_wohngebaeude

    UNION ALL

    SELECT 'Lebensmitteleinkauf - OPNV 6.84kmh',
           SUM(CASE WHEN transitwalk_1_9km_11111111_lebensmitteleinkauf THEN 1 ELSE 0 END),
           'ÖPNV',
           6.84
    FROM flurstuecke.students_wohngebaeude

    UNION ALL

    SELECT 'Lebensmitteleinkauf - Gehen 3.89kmh',
           SUM(CASE WHEN walk_1_08km_11111111_lebensmitteleinkauf THEN 1 ELSE 0 END),
           'Gehen',
           3.89
    FROM flurstuecke.students_wohngebaeude

    UNION ALL

    SELECT 'Lebensmitteleinkauf - Gehen 5.22kmh',
           SUM(CASE WHEN walk_1_45km_11111111_lebensmitteleinkauf THEN 1 ELSE 0 END),
           'Gehen',
           5.22
    FROM flurstuecke.students_wohngebaeude

    UNION ALL

    SELECT 'Lebensmitteleinkauf - Gehen 6.84kmh',
           SUM(CASE WHEN walk_1_9km_11111111_lebensmitteleinkauf THEN 1 ELSE 0 END),
           'Gehen',
           6.84
    FROM flurstuecke.students_wohngebaeude
) AS subquery

ORDER BY 
    CASE 
        WHEN Modus = 'Gehen' THEN 1 
        WHEN Modus = 'ÖPNV' THEN 2 
        WHEN Modus = 'Fahrrad' THEN 3 
    END,
    Geschwindigkeit ASC,
    Anzahl_Gebäude ASC;

	--Sport
    SELECT * FROM (
    SELECT 'Sport - Fahrrad 11.02kmh' AS Indikator, 
           SUM(CASE WHEN bicycle_3_06km_11111111_sport THEN 1 ELSE 0 END) AS Anzahl_Gebäude,
           'Fahrrad' AS Modus,
           11.02 AS Geschwindigkeit
    FROM flurstuecke.students_wohngebaeude

    UNION ALL

    SELECT 'Sport - Fahrrad 15.08kmh',
           SUM(CASE WHEN bicycle_4_19km_11111111_sport THEN 1 ELSE 0 END),
           'Fahrrad',
           15.08
    FROM flurstuecke.students_wohngebaeude

    UNION ALL

    SELECT 'Sport - Fahrrad 20.99kmh',
           SUM(CASE WHEN bicycle_5_83km_11111111_sport THEN 1 ELSE 0 END),
           'Fahrrad',
           20.99
    FROM flurstuecke.students_wohngebaeude

    UNION ALL

    SELECT 'Sport - OPNV 3.89kmh',
           SUM(CASE WHEN transitwalk_1_08km_11111111_sport THEN 1 ELSE 0 END),
           'ÖPNV',
           3.89
    FROM flurstuecke.students_wohngebaeude

    UNION ALL

    SELECT 'Sport - OPNV 5.22kmh',
           SUM(CASE WHEN transitwalk_1_45km_11111111_sport THEN 1 ELSE 0 END),
           'ÖPNV',
           5.22
    FROM flurstuecke.students_wohngebaeude

    UNION ALL

    SELECT 'Sport - OPNV 6.84kmh',
           SUM(CASE WHEN transitwalk_1_9km_11111111_sport THEN 1 ELSE 0 END),
           'ÖPNV',
           6.84
    FROM flurstuecke.students_wohngebaeude

    UNION ALL

    SELECT 'Sport - Gehen 3.89kmh',
           SUM(CASE WHEN walk_1_08km_11111111_sport THEN 1 ELSE 0 END),
           'Gehen',
           3.89
    FROM flurstuecke.students_wohngebaeude

    UNION ALL

    SELECT 'Sport - Gehen 5.22kmh',
           SUM(CASE WHEN walk_1_45km_11111111_sport THEN 1 ELSE 0 END),
           'Gehen',
           5.22
    FROM flurstuecke.students_wohngebaeude

    UNION ALL

    SELECT 'Sport - Gehen 6.84kmh',
           SUM(CASE WHEN walk_1_9km_11111111_sport THEN 1 ELSE 0 END),
           'Gehen',
           6.84
    FROM flurstuecke.students_wohngebaeude
) AS subquery

ORDER BY 
    CASE 
        WHEN Modus = 'Gehen' THEN 1 
        WHEN Modus = 'ÖPNV' THEN 2 
        WHEN Modus = 'Fahrrad' THEN 3 
    END,
    Geschwindigkeit ASC,
    Anzahl_Gebäude ASC;

--------------------------------------------------------------------------
---------- Sum up table for WALK with out main velocity 5.22kmh
SELECT * FROM (
    SELECT 'Universitäten' AS Indikator, 
           SUM(CASE WHEN walk_1_45km_11111111_universitaet THEN 1 ELSE 0 END) AS Anzahl_Gebäude
    FROM flurstuecke.students_wohngebaeude

    UNION ALL

    SELECT 'Parks',
           SUM(CASE WHEN walk_1_45km_11111111_parks THEN 1 ELSE 0 END)
    FROM flurstuecke.students_wohngebaeude

    UNION ALL

    SELECT 'Bars',
           SUM(CASE WHEN walk_1_45km_11111111_bars THEN 1 ELSE 0 END)
    FROM flurstuecke.students_wohngebaeude

    UNION ALL

    SELECT 'Clubs',
           SUM(CASE WHEN walk_1_45km_11111111_clubs THEN 1 ELSE 0 END)
    FROM flurstuecke.students_wohngebaeude

    UNION ALL

    SELECT 'Hausärzte',
           SUM(CASE WHEN walk_1_45km_11111111_hausaerzte THEN 1 ELSE 0 END)
    FROM flurstuecke.students_wohngebaeude

    UNION ALL

    SELECT 'Zahnärzte',
           SUM(CASE WHEN walk_1_45km_11111111_zahnaerzte THEN 1 ELSE 0 END)
    FROM flurstuecke.students_wohngebaeude

    UNION ALL

    SELECT 'Lebensmitteleinkauf',
           SUM(CASE WHEN walk_1_45km_11111111_lebensmitteleinkauf THEN 1 ELSE 0 END)
    FROM flurstuecke.students_wohngebaeude

    UNION ALL

    SELECT 'Sport',
           SUM(CASE WHEN walk_1_45km_11111111_sport THEN 1 ELSE 0 END)
    FROM flurstuecke.students_wohngebaeude
) AS subquery

ORDER BY Anzahl_Gebäude ASC;


-- sum up table for TRANSIT with main velocity 5.22 kmh
SELECT * FROM (
    SELECT 'Universitäten' AS Indikator, 
           SUM(CASE WHEN transitwalk_1_45km_11111111_universitaet THEN 1 ELSE 0 END) AS Anzahl_Gebäude
    FROM flurstuecke.students_wohngebaeude

    UNION ALL

    SELECT 'Parks',
           SUM(CASE WHEN transitwalk_1_45km_11111111_parks THEN 1 ELSE 0 END)
    FROM flurstuecke.students_wohngebaeude

    UNION ALL

    SELECT 'Bars',
           SUM(CASE WHEN transitwalk_1_45km_11111111_bars THEN 1 ELSE 0 END)
    FROM flurstuecke.students_wohngebaeude

    UNION ALL

    SELECT 'Clubs',
           SUM(CASE WHEN transitwalk_1_45km_11111111_clubs THEN 1 ELSE 0 END)
    FROM flurstuecke.students_wohngebaeude

    UNION ALL

    SELECT 'Hausärzte',
           SUM(CASE WHEN transitwalk_1_45km_11111111_hausaerzte THEN 1 ELSE 0 END)
    FROM flurstuecke.students_wohngebaeude

    UNION ALL

    SELECT 'Zahnärzte',
           SUM(CASE WHEN transitwalk_1_45km_11111111_zahnaerzte THEN 1 ELSE 0 END)
    FROM flurstuecke.students_wohngebaeude

    UNION ALL

    SELECT 'Lebensmitteleinkauf',
           SUM(CASE WHEN transitwalk_1_45km_11111111_lebensmitteleinkauf THEN 1 ELSE 0 END)
    FROM flurstuecke.students_wohngebaeude

    UNION ALL

    SELECT 'Sport',
           SUM(CASE WHEN transitwalk_1_45km_11111111_sport THEN 1 ELSE 0 END)
    FROM flurstuecke.students_wohngebaeude
) AS subquery

ORDER BY Anzahl_Gebäude ASC;


--sum up table for bicycle
SELECT * FROM (
    SELECT 'Universitäten' AS Indikator, 
           SUM(CASE WHEN bicycle_4_19km_11111111_universitaet THEN 1 ELSE 0 END) AS Anzahl_Gebäude
    FROM flurstuecke.students_wohngebaeude

    UNION ALL

    SELECT 'Parks',
           SUM(CASE WHEN bicycle_4_19km_11111111_parks THEN 1 ELSE 0 END)
    FROM flurstuecke.students_wohngebaeude

    UNION ALL

    SELECT 'Bars',
           SUM(CASE WHEN bicycle_4_19km_11111111_bars THEN 1 ELSE 0 END)
    FROM flurstuecke.students_wohngebaeude

    UNION ALL

    SELECT 'Clubs',
           SUM(CASE WHEN bicycle_4_19km_11111111_clubs THEN 1 ELSE 0 END)
    FROM flurstuecke.students_wohngebaeude

    UNION ALL

    SELECT 'Hausärzte',
           SUM(CASE WHEN bicycle_4_19km_11111111_hausaerzte THEN 1 ELSE 0 END)
    FROM flurstuecke.students_wohngebaeude

    UNION ALL

    SELECT 'Zahnärzte',
           SUM(CASE WHEN bicycle_4_19km_11111111_zahnaerzte THEN 1 ELSE 0 END)
    FROM flurstuecke.students_wohngebaeude

    UNION ALL

    SELECT 'Lebensmitteleinkauf',
           SUM(CASE WHEN bicycle_4_19km_11111111_lebensmitteleinkauf THEN 1 ELSE 0 END)
    FROM flurstuecke.students_wohngebaeude

    UNION ALL

    SELECT 'Sport',
           SUM(CASE WHEN bicycle_4_19km_11111111_sport THEN 1 ELSE 0 END)
    FROM flurstuecke.students_wohngebaeude
) AS subquery

ORDER BY Anzahl_Gebäude ASC;



-------------------------- KIDS NOT YET IMPLEMENTED
