WICHTIG:
Daran denken wenn man eine neue DB erstellt Postgis Extension zu aktivieren! Alles andere ist automatisiert, man muss nur die configs richtig anpassen
GetData:

1. not started yet: Google API abfragen für Arztdaten - ggf. von David

SetupDB:

1. Done: geojson2localDB --> Pfade angeben und files werden dann in tabellen + schemas hochgeladen
2. Done: changeCRS --> passt das CRS von tabellen in einem schema an
3. Done: addField --> fügt ein Feld in jede Tabelle wo der Tabellenname entweder meta oder osm enthalten hat, entsprechend ist dann auch der Feldwert

Data Processing:

1.  Done: attribute_filtering --> filtert Tabellen basierend auf einem Wert
    --> POI - Daten filtern
    --> Alkis Gebäude filter nur Wohnfunktionen- HÄNDISCH in pg admin oder so!
    --> Alkis Gebäude + Flurstuecke, filtern nach keine Wohnfunktion! - BISHER AUCH NUR HÄNDISCH

2.  not started yet: spatial_filtering --> macht den spatial join mit alkis daten

3.  not started yet: control_join --> überprüft ob die Datensätze der beiden Datenquellen den gleichen Grundstücken hinzugefügt wurden
    3.5 Sonderfall: Spielplaetze - Buffern um Spielplatzpunkt?

4.  not started yet: field_filtering --> filtert nur die relevanten felder in jeder tabelle

5.  Work in Progress: union_data --> union operation auf ausgewählte tabellen
    --> Ziel: Pro Indikator eine Tabelle aus Polygonen

6.  not started yet: create_centroid --> aus jedem Polygon den Mittelpunkt nehmen

Data Analysis:

1. not started yet

Misc:

short_filename --> passt den Namen von geojson files an
unpackzip --> entpackt zip files
util_fcts --> hilfsfunktionen, die die Umgebung einrichten

Noch ToDO

- Feldumbenennungen für ALKIS Join funktionieren nicht!
- Logger einbauen!

Ablauf

Set-Up-DB-Teil: 1. lädt alle Tabellen 2x hoch - einmal \_original und einmal die Tabelle die dann modifiziert wird 2. Modifizierte Tabellen bekommen ihr Geometriefeld angepasst mit 25832 3. Modifizierte Tabellen bekommen neue Spalte mit dem Namen der Datenquelle

Process Data Teil:

1. die ALKIS Gebäude werden custom gefiltert! Ist gehardcoded --> alle Gebaeude mit Wohnfunktion in eine neue Tabelle
2. Die To be modified Tabellen werden nach bestimmten Feldattributen gefiltert
3. Die Tabellen je Indikator werden zu einer gemeinsamen großen Tabelle UNIONed

--> Grundsätzlich ist immer der "Originalname" der Tabellenname mit dem gearbeitet werden sollte! Wenn Datenoperationen durchgeführt werden wird die "alte Version" entsprechend benannt, z.b. original, not_attr_filtered usw.!
