# Hamburg Mobility & Urban Data Platform

**Ein End-to-End-Projekt für Geodatenverarbeitung, räumliche Datenbanken, Datenqualität und interaktive Visualisierung.**

## Live Demo

### [Open the Hamburg Mobility Dashboard](https://hamburg-mobility-aram.streamlit.app)

The interactive dashboard is published using Streamlit Community Cloud to make the project accessible for demonstration and portfolio review.

It presents prepared road-network data, key indicators, charts, and road-class summaries. The dashboard is a demonstration interface for the data-analysis project, not a production traffic-monitoring service.

If the live demo is temporarily unavailable:

  - Visit the GitHub repository to review the source code, data-processing workflow, SQL analyses, and automated tests.

  - You can also try reopening the live dashboard.

## Projekt Links:

- **Dashboard:** [Streamlit Community Cloud](https://hamburg-mobility-aram.streamlit.app)
- **Source code:** [GitHub Repository](https://github.com/AramMehraban/Hamburg_Mobility_Urban_Platform)
- **Status:** Public demonstration based on prepared road-network data.

## 1. Projektziel

Dieses Projekt verarbeitet das Straßennetz Hamburgs und schafft eine nachvollziehbare Grundlage für räumliche Analysen und Mobilitätsvisualisierung.

Der Schwerpunkt liegt auf einer reproduzierbaren Datenpipeline mit Python, GeoPandas, PostgreSQL/PostGIS, SQL und Streamlit.

## 2. Aktueller Projektumfang

- Abruf von Straßennetzdaten über die offizielle Hamburger OGC-API
- Geodatenverarbeitung mit Python und GeoPandas
- Speicherung verarbeiteter Daten im Parquet-Format
- Laden der Daten in PostgreSQL mit PostGIS
- SQL-Views für Datenübersicht, Gruppierung und Kartenvisualisierung
- Qualitätsprüfungen für IDs, Geometrien und Koordinatenreferenzsysteme
- Streamlit-Dashboard mit Kennzahlen, Filtern, Diagrammen und Kartenbereich
- Automatisierte Datentests mit pytest

## 3. Technologie-Stack

| Bereich | Technologien |
|---|---|
| Programmiersprache | Python 3.11 |
| Geodatenverarbeitung | GeoPandas, Shapely |
| Dateiformat | Parquet |
| Datenbank | PostgreSQL 18, PostGIS 3.6 |
| Datenabfragen | SQL |
| Dashboard | Streamlit, PyDeck |
| Tests | pytest |
| GIS-Desktop | QGIS 3.44 |

## 4. Datenquelle und Datenqualität

**Datenquelle:** Offizielle Hamburger OGC-API für das Straßennetz.

[Hamburger Straßennetz – OGC-API](https://api.hamburg.de/datasets/v1/strassen_und_wegenetz/collections/strassennetz_gesamt/items?f=json)

Der aktuell geprüfte verarbeitete Datensatz enthält:

- 40.761 Straßensegmente
- 40.761 eindeutige Feature-IDs
- Koordinatenreferenzsystem EPSG:25832
- 0 fehlende Geometrien
- 0 leere Geometrien
- 0 ungültige Geometrien
- Geometrietyp: `LineString`

Bei einzelnen fachlichen Attributen, insbesondere Geschwindigkeitsinformationen, bestehen fehlende Werte. Diese werden nicht automatisch als fehlende Geschwindigkeitsbegrenzung interpretiert.

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
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
├── config/
│   └── database.py
├── data/
│   ├── exports/
│   └── create-view.sql
├── docs/
├── qgis/
├── reports/
│   ├── Executive_Summary.md
│   └── charts/
├── sql/
│   ├── analytics/
│   ├── ddl/
│   ├── postgresql/
│   └── qa/
├── src/
│   └── hamburg_mobility/
│       ├── app.py
│       ├── build_analytics_summaries.py
│       ├── create_charts.py
│       ├── download_roads.py
│       ├── eda.py
│       ├── export_analytics.py
│       └── load_roads_to_postgis.py
└── tests/
    └── test_road_network_data.py
```

## 7. Lokale Einrichtung

### Voraussetzungen

- Python 3.11
- PostgreSQL mit PostGIS
- Lokal eingerichtete Projektdatenbank
- QGIS (optional; für die Python-Pipeline nicht erforderlich)

### Virtuelle Umgebung erstellen

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Abhängigkeiten installieren

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## 8. Datenpipeline ausführen

Die folgenden Befehle sind für die lokale Ausführung vorgesehen. Vor einem erneuten Datenbankimport sollte geprüft werden, ob die Zieltabelle bereits Daten enthält.

### Straßennetzdaten abrufen und verarbeiten

```powershell
.\.venv\Scripts\python.exe .\src\hamburg_mobility\download_roads.py
```

### Daten in PostgreSQL/PostGIS laden

```powershell
.\.venv\Scripts\python.exe .\src\hamburg_mobility\load_roads_to_postgis.py
```

Das Importskript verwendet die Datenbank `hamburg_mobility_urban_new` und fragt das Datenbankpasswort interaktiv ab. Zugangsdaten gehören nicht in das Repository.

## 9. SQL-Analysen

Die SQL-Dateien liegen im Verzeichnis `sql/`:

- `analytics/01_road_network_overview.sql`: aggregierte Kennzahlen und Gruppierung nach Straßenattributen
- `analytics/02_road_network_map.sql`: Kartenansicht relevanter Straßenattribute und Geometrien
- `qa/01_road_network_quality_checks.sql`: Prüfungen für Datensatzumfang, IDs und Geometrien

Die Analyse-Views setzen voraus, dass die Tabelle `public.road_network` in der Zieldatenbank vorhanden ist.

## 10. Streamlit-Dashboard

Das Dashboard visualisiert vorbereitete Kennzahlen zum Hamburger Straßennetz. Die aktuelle Version verwendet die exportierte CSV-Datei `data/exports/road_network_by_class.csv`.

### Live-Dashboard öffnen

**[Hamburg Mobility Dashboard](https://hamburg-mobility-aram.streamlit.app)**

### Dashboard lokal starten

```powershell
.\.venv\Scripts\python.exe -m streamlit run .\src\hamburg_mobility\app.py
```

Die aktuelle Dashboard-Version verwendet vorbereitete CSV-Daten. PostgreSQL/PostGIS wird separat für Speicherung, Abfragen und Analysen der Geodaten eingesetzt. Eine direkte Datenbankanbindung des Dashboards wird nicht vorausgesetzt.

## 11. Automatisierte Tests

Tests aus dem Projektverzeichnis ausführen:

```powershell
.\.venv\Scripts\python.exe -m pytest .\tests -v
```

Die vorhandenen Datentests prüfen unter anderem:

- Vorhandensein der verarbeiteten Parquet-Datei
- Erwartete Anzahl von Datensätzen
- Eindeutigkeit der Feature-IDs
- Koordinatenreferenzsystem EPSG:25832
- Vorhandensein, Gültigkeit und Typ der Geometrien
- Vorhandensein wichtiger Attribute

Die Tests prüfen nicht automatisch sämtliche Datenbankoperationen oder die vollständige Funktionalität des Dashboards.

## 12. Sicherheit und Versionskontrolle

- `.venv/`, Python-Cache-Dateien und lokale Geheimnisse werden nicht versioniert.
- `data/raw/` ist in `.gitignore` ausgeschlossen.
- `.streamlit/secrets.toml` darf keine veröffentlichten Zugangsdaten enthalten.
- Passwörter und andere Geheimnisse dürfen nicht in Quellcode, Screenshots oder Git-Commits aufgenommen werden.

## 13. Geplante Erweiterungen

Die folgenden Punkte sind mögliche nächste Entwicklungsschritte und werden nicht als abgeschlossen dargestellt:

- Erweiterte Datenqualitätsberichte und Dokumentation
- Zusätzliche explorative Analysen und Jupyter-Notebooks
- Strukturierte Datenbankschemata und Staging-Prozesse
- Exportierte Kennzahlen und Daten für Power BI
- Erweiterte Tests für ETL-Prozesse und SQL-Views
- Weitere Verbesserungen der Projektdokumentation und des öffentlichen Portfolios

## 14. Projektstatus

**Lokaler Prototyp mit öffentlicher Dashboard-Demo – in Entwicklung.**

Datenverarbeitung, grundlegende Datenqualitätsprüfungen, SQL-Views und ein Streamlit-Dashboard sind vorhanden. Das veröffentlichte Dashboard basiert auf vorbereiteten Straßennetzdaten. Weitere Analysen, Tests und Dokumentation werden schrittweise ergänzt.

## Kontakt

**Aram Mehraban**

- [LinkedIn](https://www.linkedin.com/in/AramMehraban/)
- [GitHub](https://github.com/AramMehraban)
