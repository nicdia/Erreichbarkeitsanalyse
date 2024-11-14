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
