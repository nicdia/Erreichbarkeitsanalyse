SetupDB:

1. Done: geojson2localDB --> Pfade angeben und files werden dann in tabellen + schemas hochgeladen
2. Done: changeCRS --> passt das CRS von tabellen in einem schema an
3. Done: addField --> fügt ein Feld in jede Tabelle wo der Tabellenname entweder meta oder osm enthalten hat, entsprechend ist dann auch der Feldwert

Data Processing:

1.  Work in Progress: attribute_filtering --> filtert Tabellen basierend auf einem Wert
2.  Work in Progress: union_data --> union operation auf ausgewählte tabellen
3.  not started yet: spatial_filtering --> macht den spatial join mit alkis daten

Data Analysis:

1. not started yet

Misc:

short_filename --> passt den Namen von geojson files an
unpackzip --> entpackt zip files
util_fcts --> hilfsfunktionen, die die Umgebung einrichten

noch ToDo:

Arzt-Daten von Google maps api ziehen, sind nicht vorhanden
