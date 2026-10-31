# Data Quality Report – Hamburg Road Network

## 1. Zweck

Dieses Dokument fasst die bisher durchgeführten Qualitätsprüfungen des verarbeiteten Hamburger Straßennetzes zusammen.

**Geprüfte Datei:** `data/processed/hamburg_road_network_utm32.parquet`

## 2. Datensatzübersicht

| Prüfmerkmal | Ergebnis |
|---|---:|
| Datensätze | 40.761 |
| Eindeutige Feature-IDs | 40.761 |
| Fehlende Feature-IDs | 0 |
| Doppelte Feature-IDs | 0 |
| Koordinatenreferenzsystem | EPSG:25832 |
| Fehlende Geometrien | 0 |
| Leere Geometrien | 0 |
| Ungültige Geometrien | 0 |
| Geometrietyp | LineString |
| Datensätze mit LineString-Geometrie | 40.761 |

## 3. Prüfungsergebnisse

### 3.1 Vollständigkeit und Eindeutigkeit

Die geprüfte Parquet-Datei enthält 40.761 Datensätze. Die Anzahl der eindeutigen `feature_id`-Werte entspricht der Anzahl der Datensätze.

Damit wurden in der aktuellen Datei keine fehlenden oder doppelten Feature-IDs festgestellt.

### 3.2 Koordinatenreferenzsystem

Der Datensatz verwendet **ETRS89 / UTM zone 32N (EPSG:25832)**.

Das projizierte Koordinatenreferenzsystem ist für räumliche Analysen im Raum Hamburg geeignet. Bei der Darstellung in Webkarten ist gegebenenfalls eine Transformation nach EPSG:4326 erforderlich.

### 3.3 Geometriequalität

Für die aktuelle Datei wurden folgende Prüfungen durchgeführt:

- Geometrien sind vorhanden.
- Geometrien sind nicht leer.
- Geometrien sind gültig.
- Alle geprüften Geometrien sind vom Typ `LineString`.

Die Prüfungen ergaben keine festgestellten Geometriefehler.

## 4. Fehlende fachliche Attribute

Die zuvor durchgeführten Datenbankprüfungen ergaben folgende fehlende Angaben:

| Attribut | Datensätze mit fehlender Angabe |
|---|---:|
| `geschwindigkeit` | 8.803 |
| `strassenname` | 2 |
| `wegeart` | 22 |
| `strassenschluessel` | 2.710 |
| `europastrasse` | 40.686 |

Diese Werte stammen aus den bisherigen Prüfungen der Datenbanktabelle `public.road_network`. Sie sind nicht mit der Anzahl fehlender Geometrien gleichzusetzen.

**Wichtiger Hinweis:** Ein fehlender Wert in `geschwindigkeit` bedeutet nicht automatisch, dass keine Geschwindigkeitsbegrenzung existiert. Dafür ist eine fachliche Prüfung der Quelle erforderlich.

## 5. Interpretation und Grenzen

- Die Qualitätsaussagen beziehen sich auf die aktuell geprüfte lokale Datei beziehungsweise auf die zuvor geprüfte Datenbanktabelle.
- Die Prüfungen belegen nicht automatisch die Aktualität der Quelldaten.
- Die Einheit des Attributs `abschnittslaenge` wurde noch nicht anhand der Quelldokumentation verifiziert. Summen und Mittelwerte dieses Feldes sollten daher nicht ohne weitere Prüfung als Meter oder Kilometer bezeichnet werden.
- Fachliche Vollständigkeit, Aktualität und Richtigkeit einzelner Attribute müssen gesondert bewertet werden.
- Diese Prüfung ist keine vollständige Validierung sämtlicher ETL-, Datenbank- und Dashboard-Funktionen.

## 6. Automatisierte Tests

Die Datei `tests/test_road_network_data.py` enthält acht automatisierte Tests für:

- Vorhandensein der verarbeiteten Datei
- Erwartete Datensatzanzahl
- Eindeutigkeit der Feature-IDs
- EPSG:25832
- Vorhandensein und Gültigkeit der Geometrien
- Geometrietyp `LineString`
- Vorhandensein wichtiger Attribute

Bei der letzten Ausführung wurden alle acht Tests bestanden.

Ausführung:

```powershell
.\.venv\Scripts\python.exe -m pytest .\tests -v
```

## 7. Fazit

Die grundlegenden technischen Qualitätsprüfungen der aktuellen verarbeiteten Datei wurden bestanden. Insbesondere sind Datensatzanzahl, Feature-IDs, Koordinatenreferenzsystem und Geometrien konsistent mit den festgelegten Prüfkriterien.

Vor weiterführenden Mobilitätsanalysen sollten die fachlichen Bedeutungen, fehlenden Werte und Einheiten der Attribute dokumentiert werden.
