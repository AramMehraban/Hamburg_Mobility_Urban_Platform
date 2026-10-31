# Hamburg Mobility & Urban Data Platform

**Ein lokales End-to-End-Projekt für Geodatenverarbeitung, räumliche Datenbanken und interaktive Visualisierung.**

## 1. Projektziel

Dieses Projekt verarbeitet das Straßennetz Hamburgs und schafft eine nachvollziehbare Grundlage für räumliche Analysen und Mobilitätsvisualisierung.

Der Schwerpunkt liegt auf einer reproduzierbaren Datenpipeline mit Python, GeoPandas, PostgreSQL/PostGIS, SQL und Streamlit.

## 2. Aktueller Projektumfang

- Abruf von Straßennetzdaten über die offizielle Hamburger OGC-API
- Geodatenverarbeitung mit Python und GeoPandas
- Speicherung der verarbeiteten Daten im Parquet-Format
- Laden der Daten in PostgreSQL mit PostGIS
- SQL-Views für Datenübersicht, Gruppierung und Kartenvisualisierung
- Qualitätsprüfungen für IDs, Geometrien und Koordinatenreferenzsystem
- Lokales Streamlit-Dashboard mit Kennzahlen, Filtern, Diagrammen und Kartenbereich
- Automatisierte Datentests mit pytest

## 3. Technologie-Stack

| Bereich | Technologien |
|---|---|
| Programmiersprache | Python 3.11 |
| Geodaten | GeoPandas, Shapely, Parquet |
| Datenbank | PostgreSQL 18, PostGIS 3.6 |
| Datenabfrage | SQL |
| Dashboard | Streamlit, PyDeck |
| Tests | pytest |
| GIS-Desktop | QGIS 3.44 |

## 4. Datenquelle und Datenqualität

**Datenquelle:** Offizielle Hamburger OGC-API für das Straßennetz.

API:
https://api.hamburg.de/datasets/v1/strassen_und_wegenetz/collections/strassennetz_gesamt/items?f=json

Der aktuell geprüfte verarbeitete Datensatz enthält:

- 40.761 Straßensegmente
- 40.761 eindeutige Feature-IDs
- Koordinatenreferenzsystem EPSG:25832
- 0 fehlende Geometrien
- 0 leere Geometrien
- 0 ungültige Geometrien
- Geometrietyp: LineString

Bei einzelnen fachlichen Attributen, insbesondere Geschwindigkeitsinformationen, bestehen fehlende Werte. Fehlende Angaben werden nicht automatisch als fehlende Geschwindigkeitsbegrenzung interpretiert.

Die Einheit des Attributs `abschnittslaenge` muss anhand der Quelldokumentation verifiziert werden, bevor daraus fachliche Aussagen zu Metern oder Kilometern abgeleitet werden.

## 5. Datenpipeline

```text
Hamburger OGC-API
        |
        v
Python / Requests
        |
        v
GeoPandas: Prüfung und Verarbeitung
        |
        v
Parquet-Datei (EPSG:25832)
        |
        v
PostgreSQL / PostGIS
        |
        v
SQL-Views und Qualitätsprüfungen
        |
        v
Streamlit-Dashboard / PyDeck
```

## 6. Projektstruktur

```text
Hamburg_Mobility_Urban_Platform_New/
├── app.py
├── app_dashboard.py
├── app_backup_connection_test.py
├── requirements.txt
├── README.md
├── .gitignore
├── .streamlit/
├── config/
├── data/
│   ├── raw/
│   ├── processed/
│   └── exports/
├── docs/
├── notebooks/
├── powerbi/
├── qgis/
├── sql/
│   ├── analytics/
│   ├── ddl/
│   ├── qa/
│   └── staging/
├── src/
│   └── hamburg_mobility/
│       ├── download_roads.py
│       └── load_roads_to_postgis.py
└── tests/
    └── test_road_network_data.py
```

## 7. Lokale Einrichtung

Voraussetzungen:

- Python 3.11
- PostgreSQL mit PostGIS
- Eine lokal eingerichtete Projektdatenbank
- QGIS ist optional und für die Python-Pipeline nicht erforderlich.

Virtuelle Umgebung erstellen und aktivieren:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Abhängigkeiten installieren:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## 8. Datenpipeline ausführen

Die folgenden Befehle sind für die lokale Ausführung vorgesehen. Vor einem erneuten Datenbankimport sollte geprüft werden, ob die Zieltabelle bereits Daten enthält.

Verarbeitete Daten aus der offiziellen Quelle abrufen:

```powershell
.\.venv\Scripts\python.exe .\src\hamburg_mobility\download_roads.py
```

Daten in die konfigurierte PostgreSQL/PostGIS-Datenbank laden:

```powershell
.\.venv\Scripts\python.exe .\src\hamburg_mobility\load_roads_to_postgis.py
```

Das Importskript verwendet die Datenbank `hamburg_mobility_urban_new` und fragt das Datenbankpasswort interaktiv ab. Zugangsdaten gehören nicht in das Repository.

## 9. SQL-Analysen

Die SQL-Dateien liegen im Verzeichnis `sql/`:

- `analytics/01_road_network_overview.sql`: aggregierte Kennzahlen und Gruppierung nach Straßenattributen
- `analytics/02_road_network_map.sql`: Kartenansicht der relevanten Straßenattribute und Geometrien
- `qa/01_road_network_quality_checks.sql`: Prüfungen für Datensatzumfang, IDs und Geometrien

Die Analyse-Views setzen voraus, dass die Tabelle `public.road_network` in der Zieldatenbank vorhanden ist.

## 10. Streamlit-Dashboard

Das lokale Dashboard kann mit folgendem Befehl gestartet werden:

```powershell
.\.venv\Scripts\python.exe -m streamlit run .\app_dashboard.py
```

Das Dashboard greift auf PostgreSQL/PostGIS zu. Die Datenbankverbindung muss lokal eingerichtet sein. Das Passwort sollte nur über die dafür vorgesehene Eingabe eingegeben und nicht veröffentlicht werden.

## 11. Automatisierte Tests

Tests aus dem Projektverzeichnis ausführen:

```powershell
.\.venv\Scripts\python.exe -m pytest .\tests -v
```

Die aktuell vorhandenen Datentests prüfen unter anderem:

- Vorhandensein der verarbeiteten Parquet-Datei
- Erwartete Anzahl von Datensätzen
- Eindeutigkeit der Feature-IDs
- EPSG:25832
- Vorhandensein, Gültigkeit und Typ der Geometrien
- Vorhandensein wichtiger Attribute

Die Tests prüfen nicht automatisch sämtliche Datenbankoperationen oder die vollständige Funktionalität des Dashboards.

## 12. Sicherheit und Versionskontrolle

- `.venv/`, Python-Cache-Dateien und lokale Geheimnisse werden nicht versioniert.
- `data/raw/` ist in `.gitignore` ausgeschlossen.
- `.streamlit/secrets.toml` darf keine veröffentlichten Zugangsdaten enthalten.
- Passwörter und andere Geheimnisse dürfen nicht in Quellcode, Screenshots oder Git-Commits aufgenommen werden.

## 13. Geplante Erweiterungen

Die folgenden Punkte sind mögliche nächste Entwicklungsschritte und werden nicht als bereits abgeschlossen dargestellt:

- Erweiterte Datenqualitätsberichte und Dokumentation
- Zusätzliche explorative Analysen und Jupyter-Notebooks
- Strukturierte Datenbankschemata und Staging-Prozesse
- Exportierte Kennzahlen und Daten für Power BI
- Erweiterte Tests für ETL-Prozesse und SQL-Views
- Veröffentlichung einer bereinigten Projektdokumentation und eines öffentlichen Portfolios

## 14. Projektstatus

**Lokaler Prototyp – in Entwicklung.**

Datenverarbeitung, grundlegende Datenqualitätsprüfungen, SQL-Views und ein lokales Streamlit-Dashboard sind vorhanden. Weitere Analysen, Tests, Dokumentation und eine mögliche Veröffentlichung werden schrittweise ergänzt.
