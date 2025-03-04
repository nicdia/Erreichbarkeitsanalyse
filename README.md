OTP Server starten:
java -Xmx8G -jar otp.jar --router current --graphs graphs --server

WICHTIG:
Daran denken wenn man eine neue DB erstellt Postgis Extension zu aktivieren! Alles andere ist automatisiert, man muss nur die configs richtig anpassenf

Fetch Data Folder:

1. fetchGoogleMapsAPI: --> zieht von Google Maps Daten, muss man custom und individuell anpassen. An den API Key denken!
   Google Fetchen KIDS : Parks, Spielplatz, Kinderzahnarzt, Kinderarzt

SetupDB Folder (FERTIG):

1. Done: geojson2localDB --> Pfade angeben und files werden dann in tabellen + schemas hochgeladen
2. Done: changeCRS --> passt das CRS von tabellen in einem schema an
3. Done: addField --> fügt ein Feld in jede Tabelle wo der Tabellenname entweder meta oder osm enthalten hat, entsprechend ist dann auch der Feldwert

Data Processing Folder:

1.  Done: attribute_filtering --> filtert Tabellen basierend auf einem Attributswert
2.  Done: Alkis Gebäude filtern: nur Gebäude mit Wohnfunktionen
3.  Done: Union Tables --> Vereint Tabellen zu einer großen
4.  CustomIndikator Operations --> Laufend
    HÄNDISCH: Zentroide bauen

Data Analysis Folder:

1. Kommt
   Sachen die wir in der Analyse klären m+ssen: Warum kommen diese Zacken bei den isochronen? Polygone glätten?

Misc:

1. short_filename --> passt den Namen von geojson files an
2. unpackzip --> entpackt zip files
   util_fcts --> hilfsfunktionen, die die Umgebung einrichten, sind mittlerweile in jedem übergeordneten Ordner wo sie gebraucht werden

Ablauf
Set-Up-DB-Teil:

1. lädt alle Tabellen 2x hoch - einmal \_original und einmal die Tabelle die dann modifiziert wird
2. Modifizierte Tabellen bekommen ihr Geometriefeld angepasst mit 25832
3. Modifizierte Tabellen bekommen neue Spalte mit dem Namen der Datenquelle

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

DIA notes:
Datenquellen nach Indikator:
ausserschulangebote - nur metaver - Punkte - Fertig
mediallg - Kinderarzt GoogleMaps - punkte - Fertig
medispez - Kinderzahnarzt GoogleMaps - punkte - Fertig
schools - staatl. grundschulen, meta, Punkte --> Fertig
Schulische Turnhallen --> Punkte (Grundschulen mit SportHallsMeta mit Feld Schulname abgeglichen) - Fertig
naturerfahrungen - meta , polygone (wälder) + punkte (badeseen) - ZENTROIDE HÄNDISCH ERSTELLEN UND DANN UNION
parks - meta + Google Maps, Punkte --> VON GOOGLE MAPS ZIEHEN + MIT META VERSCHNEIDEN, ggf. UNION
Spielplätze - meta + osm, --> OSM Daten jedes Spielplatz Icon, Meta weniger, GMAPS auch schlecht --> NOCH ÜBERLEGEN

Daraus folgt:
Fertig: 1. Grundschulen 2. Schulische Turnhallen 3. Kinderzahnärzte 4. Kinderärzte 5. Außerschulische Angebote 6. Naturerfahrungen

Noch nicht, aber mit generischen Funktionen lösbar: 1. Naturerfahrungen (Zentroide händisch + Union Config dann noch einrichten)
Das wird komplexer: 1. Parks, 2. Spielplätze

Als nächstes zu tun (DIA):
--> Händisch Zentroid für Naturerfahrungen erstellen, dann die union config dafür einrichten
--> Skript einmal komplett von vorne bis hinten laufen lassen, damit man eine TempDB hat wo schonmal 6 Indikatoren sitzen
--> Anfangen mit Parks - überlegen wie man da vorgehen kann (siehe Parks Notizen weiter unten)
--> Irgendwann: Logger einbauen!

Notizen Parks:
OSM Daten zeigen Grünflächen
Meta Daten zeigen viele Parks aber auch Plätze, welche keine Parks sind
Google Maps Daten (Text Search und Keyword Search) zeigen auch Parks
--> Parks Vorgehen:

- Meta Daten (137 Fts.) + GMAPS Daten (60Fts) buffern - wenn in dem Radius kein OSM Punkt liegt dann ist es vermutlich ein Platz oder etwas anderes
  --> Funktioniert nicht richtig, manche Parks werden nicht genommen die eigentlich welche sind und manche Plätze die keine Parks sind werden genommen
  --> Idee: Cluster Analyse?
- gucken im Feld "name" ob Duplikate vorliegen. Wenn ja, werden die rausgeschmissen und das Ergebnis wird der Parks-Indikator

Händisch gemacht (DIA):
Zentroide erstellt für die Polygone in Naturerfahrungen, dann union ops laufen lassen

1.  Multi Polygon to Single Polygon
2.  Repair Geometry
3.  Create Centroids
4.  Change Centroid layer name
5.  Import to PostgreSQL Function - Achtung: Der Geometry-Field Name muss zum Rest passen, sonst klappt die UNION nicht!!

FESTER INDEX GRUNDSCHULKINDER

grundschulen 1 --> mit 1 gewichtet
sporthallen 2--> mit 1 gewichtet
spielplatz 3--> mit 1 gewichtet
kinderaerzte 4--> mit 1 gewichtet
kinderzanaerzte 5--> mit 1 gewichtet
parks 6--> mit 1 gewichtet
wald 7--> mit 1 gewichtet
ausserschulangebote 8 --> mit 1 gewichtet

--> ergibt das Keyword: 11111111

grundschulen 1 --> mit 3 gewichtet
sporthallen 2--> mit 5 gewichtet
spielplatz 3--> mit 7 gewichtet
kinderaerzte 4--> mit 2 gewichtet
kinderzanaerzte 5--> mit 4 gewichtet
parks 6--> mit 5 gewichtet
wald 7--> mit 6 gewichtet
ausserschulangebote 8 --> mit 2 gewichtet

--> ergibt das keyword: 3524562

Grund: Platzmangel im Feldnamen
WICHTIG: Reihenfolge der Indikatoren MUSS gleich bleiben in der Config!!

fetchApi auskommentieren --> ist noch auf 10 Features pro Tabelle eingestellt
man muss fetchApi Skript separat callen --> vorher fetch data config Tabelle anpassen
Dann die intersect Operationen kann man in main_data_processing callen, vorher drauf achten dass man config_data_processing angegeben hat

To Do 14 FEB
--> gucken ob die Intersect Ops funktionieren mit dem angepassten Fetch Data Code

--> TRANSIT, WALK, BICYCLE -->
