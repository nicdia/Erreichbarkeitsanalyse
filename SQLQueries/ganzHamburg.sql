
--------------------- First, Kids for all of Hamburg! ------------------------------
-- query walk kids how much features per score integer exist 
select 
count(*), bicycle_2_78km_11111111 as anzahl_features
from flurstuecke.kids_wohngebaeude
group by bicycle_2_78km_11111111
order by bicycle_2_78km_11111111 ASC

-- query how much features lie within 0-2, 3-5 and 6-8 range for all of Hamburg for Bicycle
select 
count (*) as feature_count,
case
when bicycle_2_78km_11111111 between 0 and 2 then 'Schlechte Erreichbarkeit'
when bicycle_2_78km_11111111 between 3 and 5 then 'Mittlere Erreichbarkeit'
when bicycle_2_78km_11111111 between 6 and 8 then 'Gute Erreichbarkeit'
else 'hier wird nix stehen'
end as Erreichbarkeitsniveau
from flurstuecke.kids_wohngebaeude
group by Erreichbarkeitsniveau
order by Erreichbarkeitsniveau ASC

--query for each calculated modus integer field, how much values get into schlecht, mittlere and gute Erreichbarkeit
SELECT ' Kind - Fahrrad 9kmh' as Modus_und_Geschwindigkeit,
       SUM(CASE WHEN bicycle_2_5km_11111111 BETWEEN 0 AND 2 THEN 1 ELSE 0 END) AS schlechte_erreichbarkeit,
       SUM(CASE WHEN bicycle_2_5km_11111111 BETWEEN 3 AND 5 THEN 1 ELSE 0 END) AS mittlere_erreichbarkeit,
       SUM(CASE WHEN bicycle_2_5km_11111111 BETWEEN 6 AND 8 THEN 1 ELSE 0 END) AS gute_erreichbarkeit
FROM flurstuecke.kids_wohngebaeude

UNION ALL

SELECT 'Kind - Fahrrad 10kmh',
       SUM(CASE WHEN bicycle_2_78km_11111111 BETWEEN 0 AND 2 THEN 1 ELSE 0 END),
       SUM(CASE WHEN bicycle_2_78km_11111111 BETWEEN 3 AND 5 THEN 1 ELSE 0 END),
       SUM(CASE WHEN bicycle_2_78km_11111111 BETWEEN 6 AND 8 THEN 1 ELSE 0 END)
FROM flurstuecke.kids_wohngebaeude

UNION ALL

SELECT 'Kind - Fahrrad 11kmh',
       SUM(CASE WHEN bicycle_3_06km_11111111 BETWEEN 0 AND 2 THEN 1 ELSE 0 END),
       SUM(CASE WHEN bicycle_3_06km_11111111 BETWEEN 3 AND 5 THEN 1 ELSE 0 END),
       SUM(CASE WHEN bicycle_3_06km_11111111 BETWEEN 6 AND 8 THEN 1 ELSE 0 END)
FROM flurstuecke.kids_wohngebaeude

UNION ALL

SELECT 'Kind - OPNV 3.53kmh',
       SUM(CASE WHEN transitwalk_0_98km_11111111 BETWEEN 0 AND 2 THEN 1 ELSE 0 END),
       SUM(CASE WHEN transitwalk_0_98km_11111111 BETWEEN 3 AND 5 THEN 1 ELSE 0 END),
       SUM(CASE WHEN transitwalk_0_98km_11111111 BETWEEN 6 AND 8 THEN 1 ELSE 0 END)
FROM flurstuecke.kids_wohngebaeude

UNION ALL

SELECT 'Kind - OPNV 4.64kmh',
       SUM(CASE WHEN transitwalk_1_29km_11111111 BETWEEN 0 AND 2 THEN 1 ELSE 0 END),
       SUM(CASE WHEN transitwalk_1_29km_11111111 BETWEEN 3 AND 5 THEN 1 ELSE 0 END),
       SUM(CASE WHEN transitwalk_1_29km_11111111 BETWEEN 6 AND 8 THEN 1 ELSE 0 END)
FROM flurstuecke.kids_wohngebaeude

UNION ALL

SELECT 'Kind - OPNV 5.98kmh',
       SUM(CASE WHEN transitwalk_1_66km_11111111 BETWEEN 0 AND 2 THEN 1 ELSE 0 END),
       SUM(CASE WHEN transitwalk_1_66km_11111111 BETWEEN 3 AND 5 THEN 1 ELSE 0 END),
       SUM(CASE WHEN transitwalk_1_66km_11111111 BETWEEN 6 AND 8 THEN 1 ELSE 0 END)
FROM flurstuecke.kids_wohngebaeude

UNION ALL

SELECT 'Kind - Gehen 3.53kmh',
       SUM(CASE WHEN walk_0_98km_11111111 BETWEEN 0 AND 2 THEN 1 ELSE 0 END),
       SUM(CASE WHEN walk_0_98km_11111111 BETWEEN 3 AND 5 THEN 1 ELSE 0 END),
       SUM(CASE WHEN walk_0_98km_11111111 BETWEEN 6 AND 8 THEN 1 ELSE 0 END)
FROM flurstuecke.kids_wohngebaeude

UNION ALL

SELECT 'Kind - Gehen 4.64kmh',
       SUM(CASE WHEN walk_1_29km_11111111 BETWEEN 0 AND 2 THEN 1 ELSE 0 END),
       SUM(CASE WHEN walk_1_29km_11111111 BETWEEN 3 AND 5 THEN 1 ELSE 0 END),
       SUM(CASE WHEN walk_1_29km_11111111 BETWEEN 6 AND 8 THEN 1 ELSE 0 END)
FROM flurstuecke.kids_wohngebaeude

UNION ALL

SELECT 'Kind - Gehen 5.98kmh',
       SUM(CASE WHEN walk_1_66km_11111111 BETWEEN 0 AND 2 THEN 1 ELSE 0 END),
       SUM(CASE WHEN walk_1_66km_11111111 BETWEEN 3 AND 5 THEN 1 ELSE 0 END),
       SUM(CASE WHEN walk_1_66km_11111111 BETWEEN 6 AND 8 THEN 1 ELSE 0 END)
FROM flurstuecke.kids_wohngebaeude

UNION ALL

SELECT 'Student - Fahrrad 11.02kmh' AS mobilitätsart,
       SUM(CASE WHEN bicycle_3_06km_11111111 BETWEEN 0 AND 2 THEN 1 ELSE 0 END) AS schlechte_erreichbarkeit,
       SUM(CASE WHEN bicycle_3_06km_11111111 BETWEEN 3 AND 5 THEN 1 ELSE 0 END) AS mittlere_erreichbarkeit,
       SUM(CASE WHEN bicycle_3_06km_11111111 BETWEEN 6 AND 8 THEN 1 ELSE 0 END) AS gute_erreichbarkeit
FROM flurstuecke.students_wohngebaeude

UNION ALL

SELECT 'Student - Fahrrad 15.08kmh',
       SUM(CASE WHEN bicycle_4_19km_11111111 BETWEEN 0 AND 2 THEN 1 ELSE 0 END),
       SUM(CASE WHEN bicycle_4_19km_11111111 BETWEEN 3 AND 5 THEN 1 ELSE 0 END),
       SUM(CASE WHEN bicycle_4_19km_11111111 BETWEEN 6 AND 8 THEN 1 ELSE 0 END)
FROM flurstuecke.students_wohngebaeude

UNION ALL

SELECT 'Student - Fahrrad 20.99kmh',
       SUM(CASE WHEN bicycle_5_83km_11111111 BETWEEN 0 AND 2 THEN 1 ELSE 0 END),
       SUM(CASE WHEN bicycle_5_83km_11111111 BETWEEN 3 AND 5 THEN 1 ELSE 0 END),
       SUM(CASE WHEN bicycle_5_83km_11111111 BETWEEN 6 AND 8 THEN 1 ELSE 0 END)
FROM flurstuecke.students_wohngebaeude

UNION ALL

SELECT 'Student - OPNV 3.89kmh' AS mobilitätsart,
       SUM(CASE WHEN transitwalk_1_08km_11111111 BETWEEN 0 AND 2 THEN 1 ELSE 0 END) AS schlechte_erreichbarkeit,
       SUM(CASE WHEN transitwalk_1_08km_11111111 BETWEEN 3 AND 5 THEN 1 ELSE 0 END) AS mittlere_erreichbarkeit,
       SUM(CASE WHEN transitwalk_1_08km_11111111 BETWEEN 6 AND 8 THEN 1 ELSE 0 END) AS gute_erreichbarkeit
FROM flurstuecke.students_wohngebaeude

UNION ALL

SELECT 'Student - OPNV 5.22kmh',
       SUM(CASE WHEN transitwalk_1_45km_11111111 BETWEEN 0 AND 2 THEN 1 ELSE 0 END),
       SUM(CASE WHEN transitwalk_1_45km_11111111 BETWEEN 3 AND 5 THEN 1 ELSE 0 END),
       SUM(CASE WHEN transitwalk_1_45km_11111111 BETWEEN 6 AND 8 THEN 1 ELSE 0 END)
FROM flurstuecke.students_wohngebaeude

UNION ALL

SELECT 'Student - OPNV 6.84kmh',
       SUM(CASE WHEN transitwalk_1_9km_11111111 BETWEEN 0 AND 2 THEN 1 ELSE 0 END),
       SUM(CASE WHEN transitwalk_1_9km_11111111 BETWEEN 3 AND 5 THEN 1 ELSE 0 END),
       SUM(CASE WHEN transitwalk_1_9km_11111111 BETWEEN 6 AND 8 THEN 1 ELSE 0 END)
FROM flurstuecke.students_wohngebaeude

UNION ALL

SELECT 'Student - Gehen 3.89kmh',
       SUM(CASE WHEN walk_1_08km_11111111 BETWEEN 0 AND 2 THEN 1 ELSE 0 END),
       SUM(CASE WHEN walk_1_08km_11111111 BETWEEN 3 AND 5 THEN 1 ELSE 0 END),
       SUM(CASE WHEN walk_1_08km_11111111 BETWEEN 6 AND 8 THEN 1 ELSE 0 END)
FROM flurstuecke.students_wohngebaeude

UNION ALL

SELECT 'Student - Gehen 5.22kmh',
       SUM(CASE WHEN walk_1_45km_11111111 BETWEEN 0 AND 2 THEN 1 ELSE 0 END),
       SUM(CASE WHEN walk_1_45km_11111111 BETWEEN 3 AND 5 THEN 1 ELSE 0 END),
       SUM(CASE WHEN walk_1_45km_11111111 BETWEEN 6 AND 8 THEN 1 ELSE 0 END)
FROM flurstuecke.students_wohngebaeude

UNION ALL

SELECT 'Student - Gehen 6.84kmh',
       SUM(CASE WHEN walk_1_9km_11111111 BETWEEN 0 AND 2 THEN 1 ELSE 0 END),
       SUM(CASE WHEN walk_1_9km_11111111 BETWEEN 3 AND 5 THEN 1 ELSE 0 END),
       SUM(CASE WHEN walk_1_9km_11111111 BETWEEN 6 AND 8 THEN 1 ELSE 0 END)
FROM flurstuecke.students_wohngebaeude
order by Modus_und_Geschwindigkeit ASC
































































------------------------ NOT WORKING YET --------------------------------------------


------------------------------- All of Hamburg with variable importance of individual indicators ----------------------

-- query feature count for each modus and speed
SELECT 'Kind - Fahrrad 9kmh' as Modus_und_Geschwindigkeit,
       SUM(CASE WHEN bicycle_2_5km_11111111 BETWEEN 0 AND 5 THEN 1 ELSE 0 END) AS schlechte_erreichbarkeit,
       SUM(CASE WHEN bicycle_2_5km_11111111 BETWEEN 6 AND 10 THEN 1 ELSE 0 END) AS mittlere_erreichbarkeit,
       SUM(CASE WHEN bicycle_2_5km_11111111 BETWEEN 11 AND 15 THEN 1 ELSE 0 END) AS gute_erreichbarkeit
FROM flurstuecke.kids_32211222_wohngebaeude

UNION ALL

SELECT 'Kind - Fahrrad 10kmh',
       SUM(CASE WHEN bicycle_2_78km_11111111 BETWEEN 0 AND 5 THEN 1 ELSE 0 END),
       SUM(CASE WHEN bicycle_2_78km_11111111 BETWEEN 6 AND 10 THEN 1 ELSE 0 END),
       SUM(CASE WHEN bicycle_2_78km_11111111 BETWEEN 11 AND 15 THEN 1 ELSE 0 END)
FROM flurstuecke.kids_32211222_wohngebaeude

UNION ALL

SELECT 'Kind - Fahrrad 11kmh',
       SUM(CASE WHEN bicycle_3_06km_11111111 BETWEEN 0 AND 5 THEN 1 ELSE 0 END),
       SUM(CASE WHEN bicycle_3_06km_11111111 BETWEEN 6 AND 10 THEN 1 ELSE 0 END),
       SUM(CASE WHEN bicycle_3_06km_11111111 BETWEEN 11 AND 15 THEN 1 ELSE 0 END)
FROM flurstuecke.kids_32211222_wohngebaeude

UNION ALL

SELECT 'Kind - OPNV 3.53kmh',
       SUM(CASE WHEN transitwalk_0_98km_11111111 BETWEEN 0 AND 5 THEN 1 ELSE 0 END),
       SUM(CASE WHEN transitwalk_0_98km_11111111 BETWEEN 6 AND 10 THEN 1 ELSE 0 END),
       SUM(CASE WHEN transitwalk_0_98km_11111111 BETWEEN 11 AND 15 THEN 1 ELSE 0 END)
FROM flurstuecke.kids_32211222_wohngebaeude

UNION ALL

SELECT 'Kind - OPNV 4.64kmh',
       SUM(CASE WHEN transitwalk_1_29km_11111111 BETWEEN 0 AND 5 THEN 1 ELSE 0 END),
       SUM(CASE WHEN transitwalk_1_29km_11111111 BETWEEN 6 AND 10 THEN 1 ELSE 0 END),
       SUM(CASE WHEN transitwalk_1_29km_11111111 BETWEEN 11 AND 15 THEN 1 ELSE 0 END)
FROM flurstuecke.kids_32211222_wohngebaeude

UNION ALL

SELECT 'Kind - OPNV 5.98kmh',
       SUM(CASE WHEN transitwalk_1_66km_11111111 BETWEEN 0 AND 5 THEN 1 ELSE 0 END),
       SUM(CASE WHEN transitwalk_1_66km_11111111 BETWEEN 6 AND 10 THEN 1 ELSE 0 END),
       SUM(CASE WHEN transitwalk_1_66km_11111111 BETWEEN 11 AND 15 THEN 1 ELSE 0 END)
FROM flurstuecke.kids_32211222_wohngebaeude

UNION ALL

SELECT 'Kind - Gehen 3.53kmh',
       SUM(CASE WHEN walk_0_98km_11111111 BETWEEN 0 AND 5 THEN 1 ELSE 0 END),
       SUM(CASE WHEN walk_0_98km_11111111 BETWEEN 6 AND 10 THEN 1 ELSE 0 END),
       SUM(CASE WHEN walk_0_98km_11111111 BETWEEN 11 AND 15 THEN 1 ELSE 0 END)
FROM flurstuecke.kids_32211222_wohngebaeude

UNION ALL

SELECT 'Kind - Gehen 4.64kmh',
       SUM(CASE WHEN walk_1_29km_11111111 BETWEEN 0 AND 5 THEN 1 ELSE 0 END),
       SUM(CASE WHEN walk_1_29km_11111111 BETWEEN 6 AND 10 THEN 1 ELSE 0 END),
       SUM(CASE WHEN walk_1_29km_11111111 BETWEEN 11 AND 15 THEN 1 ELSE 0 END)
FROM flurstuecke.kids_32211222_wohngebaeude

UNION ALL

SELECT 'Kind - Gehen 5.98kmh',
       SUM(CASE WHEN walk_1_66km_11111111 BETWEEN 0 AND 5 THEN 1 ELSE 0 END),
       SUM(CASE WHEN walk_1_66km_11111111 BETWEEN 6 AND 10 THEN 1 ELSE 0 END),
       SUM(CASE WHEN walk_1_66km_11111111 BETWEEN 11 AND 15 THEN 1 ELSE 0 END)
FROM flurstuecke.kids_32211222_wohngebaeude

UNION ALL

SELECT 'Student - Fahrrad 11.02kmh',
       SUM(CASE WHEN bicycle_3_06km_11111111 BETWEEN 0 AND 5 THEN 1 ELSE 0 END),
       SUM(CASE WHEN bicycle_3_06km_11111111 BETWEEN 6 AND 10 THEN 1 ELSE 0 END),
       SUM(CASE WHEN bicycle_3_06km_11111111 BETWEEN 11 AND 15 THEN 1 ELSE 0 END)
FROM flurstuecke.students_21132231_wohngebaeude

UNION ALL

SELECT 'Student - Fahrrad 15.08kmh',
       SUM(CASE WHEN bicycle_4_19km_11111111 BETWEEN 0 AND 5 THEN 1 ELSE 0 END),
       SUM(CASE WHEN bicycle_4_19km_11111111 BETWEEN 6 AND 10 THEN 1 ELSE 0 END),
       SUM(CASE WHEN bicycle_4_19km_11111111 BETWEEN 11 AND 15 THEN 1 ELSE 0 END)
FROM flurstuecke.students_21132231_wohngebaeude

UNION ALL

SELECT 'Student - Fahrrad 20.99kmh',
       SUM(CASE WHEN bicycle_5_83km_11111111 BETWEEN 0 AND 5 THEN 1 ELSE 0 END),
       SUM(CASE WHEN bicycle_5_83km_11111111 BETWEEN 6 AND 10 THEN 1 ELSE 0 END),
       SUM(CASE WHEN bicycle_5_83km_11111111 BETWEEN 11 AND 15 THEN 1 ELSE 0 END)
FROM flurstuecke.students_21132231_wohngebaeude

UNION ALL

SELECT 'Student - OPNV 3.89kmh',
       SUM(CASE WHEN transitwalk_1_08km_11111111 BETWEEN 0 AND 5 THEN 1 ELSE 0 END),
       SUM(CASE WHEN transitwalk_1_08km_11111111 BETWEEN 6 AND 10 THEN 1 ELSE 0 END),
       SUM(CASE WHEN transitwalk_1_08km_11111111 BETWEEN 11 AND 15 THEN 1 ELSE 0 END)
FROM flurstuecke.students_21132231_wohngebaeude

UNION ALL

SELECT 'Student - OPNV 5.22kmh',
       SUM(CASE WHEN transitwalk_1_45km_11111111 BETWEEN 0 AND 5 THEN 1 ELSE 0 END),
       SUM(CASE WHEN transitwalk_1_45km_11111111 BETWEEN 6 AND 10 THEN 1 ELSE 0 END),
       SUM(CASE WHEN transitwalk_1_45km_11111111 BETWEEN 11 AND 15 THEN 1 ELSE 0 END)
FROM flurstuecke.students_21132231_wohngebaeude

UNION ALL

SELECT 'Student - OPNV 6.84kmh',
       SUM(CASE WHEN transitwalk_1_9km_11111111 BETWEEN 0 AND 5 THEN 1 ELSE 0 END),
       SUM(CASE WHEN transitwalk_1_9km_11111111 BETWEEN 6 AND 10 THEN 1 ELSE 0 END),
       SUM(CASE WHEN transitwalk_1_9km_11111111 BETWEEN 11 AND 15 THEN 1 ELSE 0 END)
FROM flurstuecke.students_21132231_wohngebaeude

UNION ALL

SELECT 'Student - Gehen 3.89kmh',
       SUM(CASE WHEN walk_1_08km_11111111 BETWEEN 0 AND 5 THEN 1 ELSE 0 END),
       SUM(CASE WHEN walk_1_08km_11111111 BETWEEN 6 AND 10 THEN 1 ELSE 0 END),
       SUM(CASE WHEN walk_1_08km_11111111 BETWEEN 11 AND 15 THEN 1 ELSE 0 END)
FROM flurstuecke.students_21132231_wohngebaeude

UNION ALL

SELECT 'Student - Gehen 5.22kmh',
       SUM(CASE WHEN walk_1_45km_11111111 BETWEEN 0 AND 5 THEN 1 ELSE 0 END),
       SUM(CASE WHEN walk_1_45km_11111111 BETWEEN 6 AND 10 THEN 1 ELSE 0 END),
       SUM(CASE WHEN walk_1_45km_11111111 BETWEEN 11 AND 15 THEN 1 ELSE 0 END)
FROM flurstuecke.students_21132231_wohngebaeude

UNION ALL

SELECT 'Student - Gehen 5.83kmh',
       SUM(CASE WHEN walk_1_9km_11111111 BETWEEN 0 AND 5 THEN 1 ELSE 0 END),
       SUM(CASE WHEN walk_1_9km_11111111 BETWEEN 6 AND 10 THEN 1 ELSE 0 END),
       SUM(CASE WHEN walk_1_9km_11111111 BETWEEN 11 AND 15 THEN 1 ELSE 0 END)
FROM flurstuecke.students_21132231_wohngebaeude

ORDER BY Modus_und_Geschwindigkeit ASC;



