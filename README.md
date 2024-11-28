WICHTIG:
Daran denken wenn man eine neue DB erstellt Postgis Extension zu aktivieren! Alles andere ist automatisiert, man muss nur die configs richtig anpassenf

Fetch Data Folder:

1. fetchGoogleMapsAPI: --> zieht von Google Maps Daten, muss man custom und individuell anpassen. An den API Key denken!

SetupDB Folder:

1. Done: geojson2localDB --> Pfade angeben und files werden dann in tabellen + schemas hochgeladen
2. Done: changeCRS --> passt das CRS von tabellen in einem schema an
3. Done: addField --> fügt ein Feld in jede Tabelle wo der Tabellenname entweder meta oder osm enthalten hat, entsprechend ist dann auch der Feldwert

Data Processing Folder:

1.  Done: attribute_filtering --> filtert Tabellen basierend auf einem Wert
2.  Done: POI (Indikatoren) - Daten filtern nach Attributen
3.  Done: Alkis Gebäude filtern: nur Gebäude mit Wohnfunktionen

Data Analysis Folder:

1. not started yet

Misc:

1. short_filename --> passt den Namen von geojson files an
2. unpackzip --> entpackt zip files
   util_fcts --> hilfsfunktionen, die die Umgebung einrichten, sind mittlerweile in jedem übergeordneten Ordner wo sie gebraucht werden

DIA notes:
Datenquellen nach Indikator:
ausserschulangebote - nur metaver - Punkte - PASST SO NUR UNION
mediallg - Kinderarzt GoogleMaps - punkte - VON GOOGLE MAPS ZIEHEN
medispez - Kinderzahnarzt GoogleMaps - punkte - VON GOOGLE MAPS ZIEHEN
naturerfahrungen - meta , polygone (wälder) + punkte (badeseen) - ZENTROIDE ERSTELLEN UND DANN UNION
parks - meta + Google Maps, Punkte --> VON GOOGLE MAPS ZIEHEN + MIT META VERSCHNEIDEN, ggf. UNION
schools - staatl. grundschulen, meta, Punkte --> PASST SO
Spielplätze - meta + osm, --> OSM Daten jedes Spielplatz Icon, Meta weniger --> GOOGLE MAPS DATEN ZIEHEN
Schulische Turnhallen --> Punkte (Grundschulen mit SportHallsMeta mit Feld Schulname abgeglichen)

Daraus folgt:
Fertig: 1. Grundschulen 2. Schulische Turnhallen 3. Kinderzahnärzte 4. Kinderärzte

Google Fetchen: Parks, Spielplatz
Zentroide: Naturerfahrungen
UNION: Außerschulangebote, Naturerfahrungen, (Parks), (Spielplatz)

Als nächstes zu tun (DIA):
--> bessere Park und Spielplatzdaten von Google Maps ziehen (custom Field Funktion entweder mit google maps erweitern ist gehardcoded)
--> Centroid Funktion für Naturerfahrungen
--> Union Funktion schreiben
--> EVTL Da wo mehrere Datensätze für beides: Schauen wo ein Buffer um MetaverDaten gelegt werden muss um zu gucken inwiefern OSM und Metaver Daten voneinander abweichen
--> Irgendwann: Logger einbauen!

Ablauf
Set-Up-DB-Teil: 1. lädt alle Tabellen 2x hoch - einmal \_original und einmal die Tabelle die dann modifiziert wird 2. Modifizierte Tabellen bekommen ihr Geometriefeld angepasst mit 25832 3. Modifizierte Tabellen bekommen neue Spalte mit dem Namen der Datenquelle

Process Data Teil:

1. die ALKIS Gebäude werden custom gefiltert! Ist gehardcoded --> alle Gebaeude mit Wohnfunktion in eine neue Tabelle
2. Weitere Custom Funktionen (DIA: Schulische Sporthallen)
3. Die To be modified Tabellen werden nach bestimmten Feldattributen gefiltert
   -- Work in Progress --

Analyse Teil:
-- Not started yet --

Wichtig:
--> Grundsätzlich ist immer der "Originalname" der Tabellenname mit dem gearbeitet werden sollte! Wenn Datenoperationen durchgeführt werden wird die "alte Version" entsprechend benannt, z.b. original, not_attr_filtered usw.!
--> union_data: in die Liste kommen alle !Originalnamen! der Schemas, welche nicht für die UnionOps berücksichtigt werden sollen. Es werden vorher ja automatisch \_original Tabellen erstellt, die werden sowieso nicht berücksichtigt.

Funktionsspezifische Notizen:
Centroid Workflow
--> multipolygon zu singlepolygon
--> Geometrien reparieren
--> Löscher löschen
--> Sammeln, wo was fehlschlägt
