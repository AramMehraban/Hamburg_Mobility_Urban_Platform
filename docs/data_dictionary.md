# Data Dictionary – Hamburg Mobility & Urban Data Platform

## 1. Zweck

Dieses Dokument beschreibt die 22 Spalten der Tabelle
`public.road_network` in der Datenbank `hamburg_mobility_urban_new`.

Die Daten stammen aus dem Hamburger Straßen- und Wegenetz.
Die fachliche Bedeutung einzelner Felder muss bei Bedarf anhand der
offiziellen Quelldokumentation verifiziert werden.

## 2. Technische Übersicht

| Eigenschaft | Wert |
|---|---|
| Datenbank | `hamburg_mobility_urban_new` |
| Schema und Tabelle | `public.road_network` |
| Anzahl Spalten | 22 |
| Datensätze | 40.761 |
| Primärschlüssel | `feature_id` |
| Geometriespalte | `geom` |
| Geometrietyp | LineString |
| Koordinatenreferenzsystem | EPSG:25832 |

## 3. Spaltenbeschreibung

| Nr. | Spalte | PostgreSQL-Datentyp | NULL erlaubt? | Beschreibung / Interpretationshinweis |
|---:|---|---|---|---|
| 1 | `feature_id` | `bigint` | Nein | Eindeutige Feature-ID des Datensatzes; Primärschlüssel. |
| 2 | `von_netzknoten` | `text` | Ja | Kennung des Netzknotens am Anfang des Abschnitts; genaue Fachdefinition anhand der Quelldokumentation prüfen. |
| 3 | `nach_netzknoten` | `text` | Ja | Kennung des Netzknotens am Ende des Abschnitts; genaue Fachdefinition anhand der Quelldokumentation prüfen. |
| 4 | `von_station` | `bigint` | Ja | Stationswert am Anfang des Abschnitts; Einheit und genaue Bedeutung sind zu verifizieren. |
| 5 | `bis_station` | `bigint` | Ja | Stationswert am Ende des Abschnitts; Einheit und genaue Bedeutung sind zu verifizieren. |
| 6 | `klasse` | `text` | Ja | Klassifikationsmerkmal des Straßen- oder Wegeabschnitts; zulässige Werte anhand der Quelldokumentation prüfen. |
| 7 | `wegenummer` | `text` | Ja | Nummer oder Kennung des Weges; als Text belassen, bis das Format fachlich geprüft wurde. |
| 8 | `strassenname` | `text` | Ja | Straßenname, sofern in den Quelldaten vorhanden. |
| 9 | `landesschluessel` | `smallint` | Ja | Schlüsselwert auf Landesebene; fachliche Zuordnung anhand der Quelldokumentation prüfen. |
| 10 | `kreisschluessel` | `smallint` | Ja | Schlüsselwert auf Kreis- oder entsprechender Verwaltungsebene; genaue Definition prüfen. |
| 11 | `gemeindeschluessel` | `integer` | Ja | Gemeindeschlüssel; Format und fachliche Zuordnung anhand der Quelldokumentation prüfen. |
| 12 | `abschnittslaenge` | `bigint` | Ja | Längenbezogener Wert des Abschnitts. Die Einheit ist derzeit nicht verifiziert; nicht ungeprüft als Meter oder Kilometer ausgeben. |
| 13 | `ast` | `smallint` | Ja | Attribut `ast` aus dem Quelldatensatz; Bedeutung und zulässige Werte müssen anhand der Quelldokumentation geprüft werden. |
| 14 | `fahrstreifenanzahl_in_stationierungsrichtung` | `smallint` | Ja | Anzahl der Fahrstreifen in Stationierungsrichtung, sofern im Quelldatensatz angegeben. |
| 15 | `fahrstreifenanzahl_in_beide_richtungen` | `smallint` | Ja | Anzahl der Fahrstreifen in beiden Richtungen gemäß Quelldefinition; Aggregationslogik prüfen. |
| 16 | `fahrstreifenanzahl_gegen_stationierungsrichtung` | `smallint` | Ja | Anzahl der Fahrstreifen entgegen der Stationierungsrichtung, sofern angegeben. |
| 17 | `bahnigkeit` | `smallint` | Ja | Attribut zur Bahnigkeit des Abschnitts; konkrete Codierung anhand der Quelldokumentation prüfen. |
| 18 | `geschwindigkeit` | `text` | Ja | Geschwindigkeitsangabe oder entsprechender Quelltext. Enthält Textwerte; vor numerischen Analysen muss ein nachvollziehbares Bereinigungskonzept definiert werden. |
| 19 | `wegeart` | `text` | Ja | Bezeichnung oder Klassifikation der Wegeart. |
| 20 | `strassenschluessel` | `text` | Ja | Straßenschlüssel oder Straßenkennung; Format und fachliche Bedeutung prüfen. |
| 21 | `europastrasse` | `text` | Ja | Kennzeichnung oder Angabe zur Europastraße, sofern vorhanden; genaue Codierung prüfen. |
| 22 | `geom` | `geometry` | Nein | Räumliche Geometrie des Abschnitts. Erwarteter Geometrietyp: `LineString`, SRID 25832. |

## 4. Bekannte Datenqualitätsinformationen

Die folgenden Werte wurden bei den bisherigen Qualitätsprüfungen ermittelt:

| Prüfung | Ergebnis |
|---|---:|
| Datensätze | 40.761 |
| Eindeutige Feature-IDs | 40.761 |
| Fehlende oder leere Geometrien in der geprüften Tabelle | 0 |
| Ungültige Geometrien in der geprüften Tabelle | 0 |
| Fehlende Straßennamen | 2 |
| Fehlende Geschwindigkeitsinformationen | 8.803 |
| Fehlende Wegearten | 22 |
| Fehlende Straßenschlüssel | 2.710 |
| Fehlende Europastraßen-Angaben | 40.686 |

Die Anzahl fehlender Werte bezieht sich auf die bisherigen Prüfungen der Datenbanktabelle. Nach einer Änderung oder einem erneuten Import müssen diese Kennzahlen erneut geprüft werden.

## 5. Hinweise für Analysen

- `feature_id` eignet sich zur Identifikation eines Datensatzes und zur Prüfung auf Duplikate.
- `geom` ermöglicht räumliche Analysen mit PostGIS und GIS-Software.
- `geschwindigkeit` ist ein Textfeld. Eine numerische Geschwindigkeitsanalyse erfordert zunächst die Prüfung und Bereinigung der tatsächlichen Werte.
- Fehlende Geschwindigkeitsinformationen bedeuten nicht automatisch, dass für einen Abschnitt keine Geschwindigkeitsregelung existiert.
- `abschnittslaenge` darf erst nach Verifizierung der Einheit für Summen, Mittelwerte oder KPI-Beschriftungen mit einer Einheit versehen werden.
- Netz-, Stations- und Verwaltungsschlüssel sollten nicht ohne fachliche Prüfung umcodiert oder als gewöhnliche Messwerte interpretiert werden.
- Bei numerischen Attributen sind Wertebereiche und fachliche Gültigkeit zusätzlich zu prüfen.

## 6. Offene fachliche Prüfungen

Vor der endgültigen Veröffentlichung des Datenmodells sollten folgende Punkte anhand der offiziellen Quelldokumentation geklärt werden:

1. Einheit und Definition von `abschnittslaenge`.
2. Einheit und Bedeutung von `von_station` und `bis_station`.
3. Zulässige Werte und Definitionen von `klasse`, `ast` und `bahnigkeit`.
4. Codierung der Werte in `geschwindigkeit` und `europastrasse`.
5. Exakte fachliche Definition von `fahrstreifenanzahl_in_beide_richtungen`.
6. Definitionen und Formate der Netz- und Verwaltungsschlüssel.

## 7. Status

Dieses Dokument beschreibt die aktuell bekannte technische Tabellenstruktur und bereits geprüfte Datenqualitätskennzahlen. Es ersetzt nicht die offizielle fachliche Dokumentation der Datenquelle.
