
from sqlalchemy import text



def custom_elementary_sports_halls (db_con):
    """
    Erstellt die Tabelle 'sporthobbies.grundschule_sporthallen'.
    
    Die Tabelle enthält alle Sporthallen, die mit Grundschulen aus dem Schema 'schools' verknüpft sind.
    Die Verknüpfung wird über den Namen der Schule in der Spalte 'schulname' der Tabelle 'sporthobbies.sporthalle_meta' 
    und der Tabelle 'schools.grundschulen' vorgenommen.
    
    :param db_con: Verbindungsobjekt zur Datenbank
    """
    query = """
    CREATE TABLE sporthobbies.grundschule_sporthallen AS
    SELECT 
        sporthalle_meta.* 
    FROM 
        sporthobbies.sporthalle_meta 
    JOIN 
        schools.grundschulen
    ON 
        sporthalle_meta.schulname ILIKE '%' || grundschulen.schulname || '%';
    """
    try:
        with db_con.connect() as connection:
            connection.execute(text(query))
            print("Die Tabelle 'sporthobbies.grundschule_sporthallen' wurde erfolgreich erstellt.")
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")
        
def custom_parks(db_con):
    # - OSM Daten zeigen ALLE Grünflächen
    # - GMAPS und Metaver Datenssätze sind beide nicht vollständig
    #1. GMAPS und meta buffern, wenn OSM Feature drinnen liegt ist das jeweilige Feature legit --> gucken welcher Radius!!
    #2. mit den Features dann in beiden Feldern "name" gucken, ob Duplikate vorliegen. Wenn ja, werden die rausgeschmissen und das Ergebnis wird der Parks-Indikator
    pass

