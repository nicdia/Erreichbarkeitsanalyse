------------------ KIDS Queries that group by Bezirke ------------------------------
SELECT * FROM (
    SELECT 
        bezirk_name,
        'Kind - Fahrrad 10kmh' AS Modus,
        ROUND(AVG(bicycle_2_78km_11111111)) AS Durchschnittlicher_Score,
        SUM(CASE WHEN bicycle_2_78km_11111111 BETWEEN 0 AND 2 THEN 1 ELSE 0 END) AS Schlechte_Erreichbarkeit_Abs,
        ROUND((SUM(CASE WHEN bicycle_2_78km_11111111 BETWEEN 0 AND 2 THEN 1 ELSE 0 END) * 100.0) / NULLIF(COUNT(*), 0), 2) AS Schlechte_Erreichbarkeit_Proz,
        SUM(CASE WHEN bicycle_2_78km_11111111 BETWEEN 3 AND 5 THEN 1 ELSE 0 END) AS Mittlere_Erreichbarkeit_Abs,
        ROUND((SUM(CASE WHEN bicycle_2_78km_11111111 BETWEEN 3 AND 5 THEN 1 ELSE 0 END) * 100.0) / NULLIF(COUNT(*), 0), 2) AS Mittlere_Erreichbarkeit_Proz,
        SUM(CASE WHEN bicycle_2_78km_11111111 BETWEEN 6 AND 8 THEN 1 ELSE 0 END) AS Gute_Erreichbarkeit_Abs,
        ROUND((SUM(CASE WHEN bicycle_2_78km_11111111 BETWEEN 6 AND 8 THEN 1 ELSE 0 END) * 100.0) / NULLIF(COUNT(*), 0), 2) AS Gute_Erreichbarkeit_Proz,
        COUNT(*) AS Total_Gebäude
    FROM flurstuecke.kids_wohngebaeude_mit_bezirk
    GROUP BY bezirk_name

    UNION ALL

    SELECT 
        bezirk_name,
        'Kind - OPNV 4.64kmh',
        ROUND(AVG(transitwalk_1_29km_11111111)),
        SUM(CASE WHEN transitwalk_1_29km_11111111 BETWEEN 0 AND 2 THEN 1 ELSE 0 END),
        ROUND((SUM(CASE WHEN transitwalk_1_29km_11111111 BETWEEN 0 AND 2 THEN 1 ELSE 0 END) * 100.0) / NULLIF(COUNT(*), 0), 2),
        SUM(CASE WHEN transitwalk_1_29km_11111111 BETWEEN 3 AND 5 THEN 1 ELSE 0 END),
        ROUND((SUM(CASE WHEN transitwalk_1_29km_11111111 BETWEEN 3 AND 5 THEN 1 ELSE 0 END) * 100.0) / NULLIF(COUNT(*), 0), 2),
        SUM(CASE WHEN transitwalk_1_29km_11111111 BETWEEN 6 AND 8 THEN 1 ELSE 0 END),
        ROUND((SUM(CASE WHEN transitwalk_1_29km_11111111 BETWEEN 6 AND 8 THEN 1 ELSE 0 END) * 100.0) / NULLIF(COUNT(*), 0), 2),
        COUNT(*)
    FROM flurstuecke.kids_wohngebaeude_mit_bezirk
    GROUP BY bezirk_name

    UNION ALL

    SELECT 
        bezirk_name,
        'Kind - Gehen 4.64kmh',
        ROUND(AVG(walk_1_29km_11111111)),
        SUM(CASE WHEN walk_1_29km_11111111 BETWEEN 0 AND 2 THEN 1 ELSE 0 END),
        ROUND((SUM(CASE WHEN walk_1_29km_11111111 BETWEEN 0 AND 2 THEN 1 ELSE 0 END) * 100.0) / NULLIF(COUNT(*), 0), 2),
        SUM(CASE WHEN walk_1_29km_11111111 BETWEEN 3 AND 5 THEN 1 ELSE 0 END),
        ROUND((SUM(CASE WHEN walk_1_29km_11111111 BETWEEN 3 AND 5 THEN 1 ELSE 0 END) * 100.0) / NULLIF(COUNT(*), 0), 2),
        SUM(CASE WHEN walk_1_29km_11111111 BETWEEN 6 AND 8 THEN 1 ELSE 0 END),
        ROUND((SUM(CASE WHEN walk_1_29km_11111111 BETWEEN 6 AND 8 THEN 1 ELSE 0 END) * 100.0) / NULLIF(COUNT(*), 0), 2),
        COUNT(*)
    FROM flurstuecke.kids_wohngebaeude_mit_bezirk
    GROUP BY bezirk_name
) AS subquery
WHERE bezirk_name IS NOT NULL
ORDER BY 
    Durchschnittlicher_Score ASC,
    CASE 
        WHEN Modus LIKE '%Gehen%' THEN 1 
        WHEN Modus LIKE '%OPNV%' THEN 2 
        WHEN Modus LIKE '%Fahrrad%' THEN 3 
    END,
    Durchschnittlicher_Score ASC;

-- join it with bezirke datensatz
SELECT * FROM (
    SELECT 
        k.bezirk_name,
        'Kind - Fahrrad 10kmh' AS Modus,
        ROUND(AVG(bicycle_2_78km_11111111)) AS Durchschnittlicher_Score,
        SUM(CASE WHEN bicycle_2_78km_11111111 BETWEEN 0 AND 2 THEN 1 ELSE 0 END) AS Schlechte_Erreichbarkeit_Abs,
        ROUND((SUM(CASE WHEN bicycle_2_78km_11111111 BETWEEN 0 AND 2 THEN 1 ELSE 0 END) * 100.0) / NULLIF(COUNT(*), 0), 2) AS Schlechte_Erreichbarkeit_Proz,
        SUM(CASE WHEN bicycle_2_78km_11111111 BETWEEN 3 AND 5 THEN 1 ELSE 0 END) AS Mittlere_Erreichbarkeit_Abs,
        ROUND((SUM(CASE WHEN bicycle_2_78km_11111111 BETWEEN 3 AND 5 THEN 1 ELSE 0 END) * 100.0) / NULLIF(COUNT(*), 0), 2) AS Mittlere_Erreichbarkeit_Proz,
        SUM(CASE WHEN bicycle_2_78km_11111111 BETWEEN 6 AND 8 THEN 1 ELSE 0 END) AS Gute_Erreichbarkeit_Abs,
        ROUND((SUM(CASE WHEN bicycle_2_78km_11111111 BETWEEN 6 AND 8 THEN 1 ELSE 0 END) * 100.0) / NULLIF(COUNT(*), 0), 2) AS Gute_Erreichbarkeit_Proz,
        COUNT(*) AS Total_Gebäude
    FROM flurstuecke.kids_wohngebaeude_mit_bezirk k
    GROUP BY k.bezirk_name

    UNION ALL

    SELECT 
        k.bezirk_name,
        'Kind - OPNV 4.64kmh',
        ROUND(AVG(transitwalk_1_29km_11111111)),
        SUM(CASE WHEN transitwalk_1_29km_11111111 BETWEEN 0 AND 2 THEN 1 ELSE 0 END),
        ROUND((SUM(CASE WHEN transitwalk_1_29km_11111111 BETWEEN 0 AND 2 THEN 1 ELSE 0 END) * 100.0) / NULLIF(COUNT(*), 0), 2),
        SUM(CASE WHEN transitwalk_1_29km_11111111 BETWEEN 3 AND 5 THEN 1 ELSE 0 END),
        ROUND((SUM(CASE WHEN transitwalk_1_29km_11111111 BETWEEN 3 AND 5 THEN 1 ELSE 0 END) * 100.0) / NULLIF(COUNT(*), 0), 2),
        SUM(CASE WHEN transitwalk_1_29km_11111111 BETWEEN 6 AND 8 THEN 1 ELSE 0 END),
        ROUND((SUM(CASE WHEN transitwalk_1_29km_11111111 BETWEEN 6 AND 8 THEN 1 ELSE 0 END) * 100.0) / NULLIF(COUNT(*), 0), 2),
        COUNT(*)
    FROM flurstuecke.kids_wohngebaeude_mit_bezirk k
    GROUP BY k.bezirk_name

    UNION ALL

    SELECT 
        k.bezirk_name,
        'Kind - Gehen 4.64kmh',
        ROUND(AVG(walk_1_29km_11111111)),
        SUM(CASE WHEN walk_1_29km_11111111 BETWEEN 0 AND 2 THEN 1 ELSE 0 END),
        ROUND((SUM(CASE WHEN walk_1_29km_11111111 BETWEEN 0 AND 2 THEN 1 ELSE 0 END) * 100.0) / NULLIF(COUNT(*), 0), 2),
        SUM(CASE WHEN walk_1_29km_11111111 BETWEEN 3 AND 5 THEN 1 ELSE 0 END),
        ROUND((SUM(CASE WHEN walk_1_29km_11111111 BETWEEN 3 AND 5 THEN 1 ELSE 0 END) * 100.0) / NULLIF(COUNT(*), 0), 2),
        SUM(CASE WHEN walk_1_29km_11111111 BETWEEN 6 AND 8 THEN 1 ELSE 0 END),
        ROUND((SUM(CASE WHEN walk_1_29km_11111111 BETWEEN 6 AND 8 THEN 1 ELSE 0 END) * 100.0) / NULLIF(COUNT(*), 0), 2),
        COUNT(*)
    FROM flurstuecke.kids_wohngebaeude_mit_bezirk k
    GROUP BY k.bezirk_name
) AS subquery
JOIN bezirksgrenzen_gemarkungen.bezirke b ON subquery.bezirk_name = b.bezirk_name
WHERE subquery.bezirk_name IS NOT NULL
ORDER BY 
    subquery.bezirk_name ASC,
    CASE 
        WHEN subquery.Modus LIKE '%Gehen%' THEN 1 
        WHEN subquery.Modus LIKE '%OPNV%' THEN 2 
        WHEN subquery.Modus LIKE '%Fahrrad%' THEN 3 
    END,
    subquery.Durchschnittlicher_Score ASC;
	
--- final query that takes the averages to get final ratings for each bezirk
SELECT 
    b.bezirk_name,
    ROUND(AVG(subquery.Durchschnittlicher_Score)) AS Durchschnittlicher_Score,
    ROUND(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY subquery.Durchschnittlicher_Score)) AS Median_Score,
    
    ROUND(AVG(subquery.Schlechte_Erreichbarkeit_Abs)) AS Schlechte_Erreichbarkeit_Abs,
    ROUND(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY subquery.Schlechte_Erreichbarkeit_Abs)) AS Median_Schlechte_Abs,
    ROUND(AVG(subquery.Schlechte_Erreichbarkeit_Proz), 2) AS Schlechte_Erreichbarkeit_Proz,
    ROUND(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY subquery.Schlechte_Erreichbarkeit_Proz)) AS Median_Schlechte_Proz,

    ROUND(AVG(subquery.Mittlere_Erreichbarkeit_Abs)) AS Mittlere_Erreichbarkeit_Abs,
    ROUND(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY subquery.Mittlere_Erreichbarkeit_Abs)) AS Median_Mittlere_Abs,
    ROUND(AVG(subquery.Mittlere_Erreichbarkeit_Proz), 2) AS Mittlere_Erreichbarkeit_Proz,
    ROUND(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY subquery.Mittlere_Erreichbarkeit_Proz)) AS Median_Mittlere_Proz,

    ROUND(AVG(subquery.Gute_Erreichbarkeit_Abs)) AS Gute_Erreichbarkeit_Abs,
    ROUND(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY subquery.Gute_Erreichbarkeit_Abs)) AS Median_Gute_Abs,
    ROUND(AVG(subquery.Gute_Erreichbarkeit_Proz), 2) AS Gute_Erreichbarkeit_Proz,
    ROUND(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY subquery.Gute_Erreichbarkeit_Proz)) AS Median_Gute_Proz,

    SUM(subquery.Total_Gebäude) AS Total_Gebäude,
    b.geometry
FROM (
    SELECT 
        k.bezirk_name,
        ROUND(AVG(bicycle_2_78km_11111111)) AS Durchschnittlicher_Score,
        SUM(CASE WHEN bicycle_2_78km_11111111 BETWEEN 0 AND 2 THEN 1 ELSE 0 END) AS Schlechte_Erreichbarkeit_Abs,
        ROUND((SUM(CASE WHEN bicycle_2_78km_11111111 BETWEEN 0 AND 2 THEN 1 ELSE 0 END) * 100.0) / NULLIF(COUNT(*), 0), 2) AS Schlechte_Erreichbarkeit_Proz,
        SUM(CASE WHEN bicycle_2_78km_11111111 BETWEEN 3 AND 5 THEN 1 ELSE 0 END) AS Mittlere_Erreichbarkeit_Abs,
        ROUND((SUM(CASE WHEN bicycle_2_78km_11111111 BETWEEN 3 AND 5 THEN 1 ELSE 0 END) * 100.0) / NULLIF(COUNT(*), 0), 2) AS Mittlere_Erreichbarkeit_Proz,
        SUM(CASE WHEN bicycle_2_78km_11111111 BETWEEN 6 AND 8 THEN 1 ELSE 0 END) AS Gute_Erreichbarkeit_Abs,
        ROUND((SUM(CASE WHEN bicycle_2_78km_11111111 BETWEEN 6 AND 8 THEN 1 ELSE 0 END) * 100.0) / NULLIF(COUNT(*), 0), 2) AS Gute_Erreichbarkeit_Proz,
        COUNT(*) AS Total_Gebäude
    FROM flurstuecke.kids_wohngebaeude_mit_bezirk k
    GROUP BY k.bezirk_name

    UNION ALL

    SELECT 
        k.bezirk_name,
        ROUND(AVG(transitwalk_1_29km_11111111)),
        SUM(CASE WHEN transitwalk_1_29km_11111111 BETWEEN 0 AND 2 THEN 1 ELSE 0 END),
        ROUND((SUM(CASE WHEN transitwalk_1_29km_11111111 BETWEEN 0 AND 2 THEN 1 ELSE 0 END) * 100.0) / NULLIF(COUNT(*), 0), 2),
        SUM(CASE WHEN transitwalk_1_29km_11111111 BETWEEN 3 AND 5 THEN 1 ELSE 0 END),
        ROUND((SUM(CASE WHEN transitwalk_1_29km_11111111 BETWEEN 3 AND 5 THEN 1 ELSE 0 END) * 100.0) / NULLIF(COUNT(*), 0), 2),
        SUM(CASE WHEN transitwalk_1_29km_11111111 BETWEEN 6 AND 8 THEN 1 ELSE 0 END),
        ROUND((SUM(CASE WHEN transitwalk_1_29km_11111111 BETWEEN 6 AND 8 THEN 1 ELSE 0 END) * 100.0) / NULLIF(COUNT(*), 0), 2),
        COUNT(*)
    FROM flurstuecke.kids_wohngebaeude_mit_bezirk k
    GROUP BY k.bezirk_name

    UNION ALL

    SELECT 
        k.bezirk_name,
        ROUND(AVG(walk_1_29km_11111111)),
        SUM(CASE WHEN walk_1_29km_11111111 BETWEEN 0 AND 2 THEN 1 ELSE 0 END),
        ROUND((SUM(CASE WHEN walk_1_29km_11111111 BETWEEN 0 AND 2 THEN 1 ELSE 0 END) * 100.0) / NULLIF(COUNT(*), 0), 2),
        SUM(CASE WHEN walk_1_29km_11111111 BETWEEN 3 AND 5 THEN 1 ELSE 0 END),
        ROUND((SUM(CASE WHEN walk_1_29km_11111111 BETWEEN 3 AND 5 THEN 1 ELSE 0 END) * 100.0) / NULLIF(COUNT(*), 0), 2),
        SUM(CASE WHEN walk_1_29km_11111111 BETWEEN 6 AND 8 THEN 1 ELSE 0 END),
        ROUND((SUM(CASE WHEN walk_1_29km_11111111 BETWEEN 6 AND 8 THEN 1 ELSE 0 END) * 100.0) / NULLIF(COUNT(*), 0), 2),
        COUNT(*)
    FROM flurstuecke.kids_wohngebaeude_mit_bezirk k
    GROUP BY k.bezirk_name
) AS subquery
JOIN bezirksgrenzen_gemarkungen.bezirke b ON subquery.bezirk_name = b.bezirk_name
GROUP BY b.bezirk_name, b.geometry
ORDER BY Durchschnittlicher_Score ASC;

------------------ STUDENTS Queries that group by Bezirke ------------------------------
SELECT * FROM (
    SELECT 
        bezirk_name,
        'Student - Fahrrad 15.08kmh' AS Modus,
        ROUND(AVG(bicycle_4_19km_11111111)) AS Durchschnittlicher_Score,
        SUM(CASE WHEN bicycle_4_19km_11111111 BETWEEN 0 AND 2 THEN 1 ELSE 0 END) AS Schlechte_Erreichbarkeit_Abs,
        ROUND((SUM(CASE WHEN bicycle_4_19km_11111111 BETWEEN 0 AND 2 THEN 1 ELSE 0 END) * 100.0) / NULLIF(COUNT(*), 0), 2) AS Schlechte_Erreichbarkeit_Proz,
        SUM(CASE WHEN bicycle_4_19km_11111111 BETWEEN 3 AND 5 THEN 1 ELSE 0 END) AS Mittlere_Erreichbarkeit_Abs,
        ROUND((SUM(CASE WHEN bicycle_4_19km_11111111 BETWEEN 3 AND 5 THEN 1 ELSE 0 END) * 100.0) / NULLIF(COUNT(*), 0), 2) AS Mittlere_Erreichbarkeit_Proz,
        SUM(CASE WHEN bicycle_4_19km_11111111 BETWEEN 6 AND 8 THEN 1 ELSE 0 END) AS Gute_Erreichbarkeit_Abs,
        ROUND((SUM(CASE WHEN bicycle_4_19km_11111111 BETWEEN 6 AND 8 THEN 1 ELSE 0 END) * 100.0) / NULLIF(COUNT(*), 0), 2) AS Gute_Erreichbarkeit_Proz,
        COUNT(*) AS Total_Gebäude
    FROM flurstuecke.students_wohngebaeude_mit_bezirk
    GROUP BY bezirk_name

    UNION ALL

    SELECT 
        bezirk_name,
        'Student - OPNV 5.22kmh',
        ROUND(AVG(transitwalk_1_45km_11111111)),
        SUM(CASE WHEN transitwalk_1_45km_11111111 BETWEEN 0 AND 2 THEN 1 ELSE 0 END),
        ROUND((SUM(CASE WHEN transitwalk_1_45km_11111111 BETWEEN 0 AND 2 THEN 1 ELSE 0 END) * 100.0) / NULLIF(COUNT(*), 0), 2),
        SUM(CASE WHEN transitwalk_1_45km_11111111 BETWEEN 3 AND 5 THEN 1 ELSE 0 END),
        ROUND((SUM(CASE WHEN transitwalk_1_45km_11111111 BETWEEN 3 AND 5 THEN 1 ELSE 0 END) * 100.0) / NULLIF(COUNT(*), 0), 2),
        SUM(CASE WHEN transitwalk_1_45km_11111111 BETWEEN 6 AND 8 THEN 1 ELSE 0 END),
        ROUND((SUM(CASE WHEN transitwalk_1_45km_11111111 BETWEEN 6 AND 8 THEN 1 ELSE 0 END) * 100.0) / NULLIF(COUNT(*), 0), 2),
        COUNT(*)
    FROM flurstuecke.students_wohngebaeude_mit_bezirk
    GROUP BY bezirk_name

    UNION ALL

    SELECT 
        bezirk_name,
        'Student - Gehen 5.22kmh',
        ROUND(AVG(walk_1_45km_11111111)),
        SUM(CASE WHEN walk_1_45km_11111111 BETWEEN 0 AND 2 THEN 1 ELSE 0 END),
        ROUND((SUM(CASE WHEN walk_1_45km_11111111 BETWEEN 0 AND 2 THEN 1 ELSE 0 END) * 100.0) / NULLIF(COUNT(*), 0), 2),
        SUM(CASE WHEN walk_1_45km_11111111 BETWEEN 3 AND 5 THEN 1 ELSE 0 END),
        ROUND((SUM(CASE WHEN walk_1_45km_11111111 BETWEEN 3 AND 5 THEN 1 ELSE 0 END) * 100.0) / NULLIF(COUNT(*), 0), 2),
        SUM(CASE WHEN walk_1_45km_11111111 BETWEEN 6 AND 8 THEN 1 ELSE 0 END),
        ROUND((SUM(CASE WHEN walk_1_45km_11111111 BETWEEN 6 AND 8 THEN 1 ELSE 0 END) * 100.0) / NULLIF(COUNT(*), 0), 2),
        COUNT(*)
    FROM flurstuecke.students_wohngebaeude_mit_bezirk
    GROUP BY bezirk_name
) AS subquery
JOIN bezirksgrenzen_gemarkungen.bezirke b ON subquery.bezirk_name = b.bezirk_name
WHERE subquery.bezirk_name IS NOT NULL
ORDER BY 
	subquery.Durchschnittlicher_Score ASC,
    subquery.bezirk_name ASC,
    CASE 
        WHEN subquery.Modus LIKE '%Gehen%' THEN 1 
        WHEN subquery.Modus LIKE '%OPNV%' THEN 2 
        WHEN subquery.Modus LIKE '%Fahrrad%' THEN 3 
    END;
	
-- join that with bezirke
SELECT * FROM (
    SELECT 
        k.bezirk_name,
        'Student - Fahrrad 15.08kmh' AS Modus,
        ROUND(AVG(bicycle_4_19km_11111111)) AS Durchschnittlicher_Score,
        SUM(CASE WHEN bicycle_4_19km_11111111 BETWEEN 0 AND 2 THEN 1 ELSE 0 END) AS Schlechte_Erreichbarkeit_Abs,
        ROUND((SUM(CASE WHEN bicycle_4_19km_11111111 BETWEEN 0 AND 2 THEN 1 ELSE 0 END) * 100.0) / NULLIF(COUNT(*), 0), 2) AS Schlechte_Erreichbarkeit_Proz,
        SUM(CASE WHEN bicycle_4_19km_11111111 BETWEEN 3 AND 5 THEN 1 ELSE 0 END) AS Mittlere_Erreichbarkeit_Abs,
        ROUND((SUM(CASE WHEN bicycle_4_19km_11111111 BETWEEN 3 AND 5 THEN 1 ELSE 0 END) * 100.0) / NULLIF(COUNT(*), 0), 2) AS Mittlere_Erreichbarkeit_Proz,
        SUM(CASE WHEN bicycle_4_19km_11111111 BETWEEN 6 AND 8 THEN 1 ELSE 0 END) AS Gute_Erreichbarkeit_Abs,
        ROUND((SUM(CASE WHEN bicycle_4_19km_11111111 BETWEEN 6 AND 8 THEN 1 ELSE 0 END) * 100.0) / NULLIF(COUNT(*), 0), 2) AS Gute_Erreichbarkeit_Proz,
        COUNT(*) AS Total_Gebäude
    FROM flurstuecke.students_wohngebaeude_mit_bezirk k
    GROUP BY k.bezirk_name

    UNION ALL

    SELECT 
        k.bezirk_name,
        'Student - OPNV 5.22kmh',
        ROUND(AVG(transitwalk_1_45km_11111111)),
        SUM(CASE WHEN transitwalk_1_45km_11111111 BETWEEN 0 AND 2 THEN 1 ELSE 0 END),
        ROUND((SUM(CASE WHEN transitwalk_1_45km_11111111 BETWEEN 0 AND 2 THEN 1 ELSE 0 END) * 100.0) / NULLIF(COUNT(*), 0), 2),
        SUM(CASE WHEN transitwalk_1_45km_11111111 BETWEEN 3 AND 5 THEN 1 ELSE 0 END),
        ROUND((SUM(CASE WHEN transitwalk_1_45km_11111111 BETWEEN 3 AND 5 THEN 1 ELSE 0 END) * 100.0) / NULLIF(COUNT(*), 0), 2),
        SUM(CASE WHEN transitwalk_1_45km_11111111 BETWEEN 6 AND 8 THEN 1 ELSE 0 END),
        ROUND((SUM(CASE WHEN transitwalk_1_45km_11111111 BETWEEN 6 AND 8 THEN 1 ELSE 0 END) * 100.0) / NULLIF(COUNT(*), 0), 2),
        COUNT(*)
    FROM flurstuecke.students_wohngebaeude_mit_bezirk k
    GROUP BY k.bezirk_name

    UNION ALL

    SELECT 
        k.bezirk_name,
        'Student - Gehen 5.22kmh',
        ROUND(AVG(walk_1_45km_11111111)),
        SUM(CASE WHEN walk_1_45km_11111111 BETWEEN 0 AND 2 THEN 1 ELSE 0 END),
        ROUND((SUM(CASE WHEN walk_1_45km_11111111 BETWEEN 0 AND 2 THEN 1 ELSE 0 END) * 100.0) / NULLIF(COUNT(*), 0), 2),
        SUM(CASE WHEN walk_1_45km_11111111 BETWEEN 3 AND 5 THEN 1 ELSE 0 END),
        ROUND((SUM(CASE WHEN walk_1_45km_11111111 BETWEEN 3 AND 5 THEN 1 ELSE 0 END) * 100.0) / NULLIF(COUNT(*), 0), 2),
        SUM(CASE WHEN walk_1_45km_11111111 BETWEEN 6 AND 8 THEN 1 ELSE 0 END),
        ROUND((SUM(CASE WHEN walk_1_45km_11111111 BETWEEN 6 AND 8 THEN 1 ELSE 0 END) * 100.0) / NULLIF(COUNT(*), 0), 2),
        COUNT(*)
    FROM flurstuecke.students_wohngebaeude_mit_bezirk k
    GROUP BY k.bezirk_name
) AS subquery
JOIN bezirksgrenzen_gemarkungen.bezirke b ON subquery.bezirk_name = b.bezirk_name
WHERE subquery.bezirk_name IS NOT NULL
ORDER BY 
    subquery.bezirk_name ASC,
    CASE 
        WHEN subquery.Modus LIKE '%Gehen%' THEN 1 
        WHEN subquery.Modus LIKE '%OPNV%' THEN 2 
        WHEN subquery.Modus LIKE '%Fahrrad%' THEN 3 
    END,
    subquery.Durchschnittlicher_Score ASC;
	
	
-- final aggregation for students
SELECT 
    b.bezirk_name,
    ROUND(AVG(subquery.Durchschnittlicher_Score)) AS Durchschnittlicher_Score,
    ROUND(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY subquery.Durchschnittlicher_Score)) AS Median_Score,
    
    ROUND(AVG(subquery.Schlechte_Erreichbarkeit_Abs)) AS Schlechte_Erreichbarkeit_Abs,
    ROUND(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY subquery.Schlechte_Erreichbarkeit_Abs)) AS Median_Schlechte_Abs,
    ROUND(AVG(subquery.Schlechte_Erreichbarkeit_Proz), 2) AS Schlechte_Erreichbarkeit_Proz,
    ROUND(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY subquery.Schlechte_Erreichbarkeit_Proz)) AS Median_Schlechte_Proz,

    ROUND(AVG(subquery.Mittlere_Erreichbarkeit_Abs)) AS Mittlere_Erreichbarkeit_Abs,
    ROUND(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY subquery.Mittlere_Erreichbarkeit_Abs)) AS Median_Mittlere_Abs,
    ROUND(AVG(subquery.Mittlere_Erreichbarkeit_Proz), 2) AS Mittlere_Erreichbarkeit_Proz,
    ROUND(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY subquery.Mittlere_Erreichbarkeit_Proz)) AS Median_Mittlere_Proz,

    ROUND(AVG(subquery.Gute_Erreichbarkeit_Abs)) AS Gute_Erreichbarkeit_Abs,
    ROUND(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY subquery.Gute_Erreichbarkeit_Abs)) AS Median_Gute_Abs,
    ROUND(AVG(subquery.Gute_Erreichbarkeit_Proz), 2) AS Gute_Erreichbarkeit_Proz,
    ROUND(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY subquery.Gute_Erreichbarkeit_Proz)) AS Median_Gute_Proz,

    SUM(subquery.Total_Gebäude) AS Total_Gebäude,
    b.geometry
FROM (
    SELECT 
        k.bezirk_name,
        ROUND(AVG(bicycle_4_19km_11111111)) AS Durchschnittlicher_Score,
        SUM(CASE WHEN bicycle_4_19km_11111111 BETWEEN 0 AND 2 THEN 1 ELSE 0 END) AS Schlechte_Erreichbarkeit_Abs,
        ROUND((SUM(CASE WHEN bicycle_4_19km_11111111 BETWEEN 0 AND 2 THEN 1 ELSE 0 END) * 100.0) / NULLIF(COUNT(*), 0), 2) AS Schlechte_Erreichbarkeit_Proz,
        SUM(CASE WHEN bicycle_4_19km_11111111 BETWEEN 3 AND 5 THEN 1 ELSE 0 END) AS Mittlere_Erreichbarkeit_Abs,
        ROUND((SUM(CASE WHEN bicycle_4_19km_11111111 BETWEEN 3 AND 5 THEN 1 ELSE 0 END) * 100.0) / NULLIF(COUNT(*), 0), 2) AS Mittlere_Erreichbarkeit_Proz,
        SUM(CASE WHEN bicycle_4_19km_11111111 BETWEEN 6 AND 8 THEN 1 ELSE 0 END) AS Gute_Erreichbarkeit_Abs,
        ROUND((SUM(CASE WHEN bicycle_4_19km_11111111 BETWEEN 6 AND 8 THEN 1 ELSE 0 END) * 100.0) / NULLIF(COUNT(*), 0), 2) AS Gute_Erreichbarkeit_Proz,
        COUNT(*) AS Total_Gebäude
    FROM flurstuecke.students_wohngebaeude_mit_bezirk k
    GROUP BY k.bezirk_name

    UNION ALL

    SELECT 
        k.bezirk_name,
        ROUND(AVG(transitwalk_1_45km_11111111)),
        SUM(CASE WHEN transitwalk_1_45km_11111111 BETWEEN 0 AND 2 THEN 1 ELSE 0 END),
        ROUND((SUM(CASE WHEN transitwalk_1_45km_11111111 BETWEEN 0 AND 2 THEN 1 ELSE 0 END) * 100.0) / NULLIF(COUNT(*), 0), 2),
        SUM(CASE WHEN transitwalk_1_45km_11111111 BETWEEN 3 AND 5 THEN 1 ELSE 0 END),
        ROUND((SUM(CASE WHEN transitwalk_1_45km_11111111 BETWEEN 3 AND 5 THEN 1 ELSE 0 END) * 100.0) / NULLIF(COUNT(*), 0), 2),
        SUM(CASE WHEN transitwalk_1_45km_11111111 BETWEEN 6 AND 8 THEN 1 ELSE 0 END),
        ROUND((SUM(CASE WHEN transitwalk_1_45km_11111111 BETWEEN 6 AND 8 THEN 1 ELSE 0 END) * 100.0) / NULLIF(COUNT(*), 0), 2),
        COUNT(*)
    FROM flurstuecke.students_wohngebaeude_mit_bezirk k
    GROUP BY k.bezirk_name

    UNION ALL

    SELECT 
        k.bezirk_name,
        ROUND(AVG(walk_1_45km_11111111)),
        SUM(CASE WHEN walk_1_45km_11111111 BETWEEN 0 AND 2 THEN 1 ELSE 0 END),
        ROUND((SUM(CASE WHEN walk_1_45km_11111111 BETWEEN 0 AND 2 THEN 1 ELSE 0 END) * 100.0) / NULLIF(COUNT(*), 0), 2),
        SUM(CASE WHEN walk_1_45km_11111111 BETWEEN 3 AND 5 THEN 1 ELSE 0 END),
        ROUND((SUM(CASE WHEN walk_1_45km_11111111 BETWEEN 3 AND 5 THEN 1 ELSE 0 END) * 100.0) / NULLIF(COUNT(*), 0), 2),
        SUM(CASE WHEN walk_1_45km_11111111 BETWEEN 6 AND 8 THEN 1 ELSE 0 END),
        ROUND((SUM(CASE WHEN walk_1_45km_11111111 BETWEEN 6 AND 8 THEN 1 ELSE 0 END) * 100.0) / NULLIF(COUNT(*), 0), 2),
        COUNT(*)
    FROM flurstuecke.students_wohngebaeude_mit_bezirk k
    GROUP BY k.bezirk_name
) AS subquery
JOIN bezirksgrenzen_gemarkungen.bezirke b ON subquery.bezirk_name = b.bezirk_name
GROUP BY b.bezirk_name, b.geometry
ORDER BY Durchschnittlicher_Score ASC;

