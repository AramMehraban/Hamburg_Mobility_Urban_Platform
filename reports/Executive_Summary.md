# Hamburg Mobility & Urban Data Platform

## 1. Projektziel

Ziel dieses Projekts ist es, ein nachvollziehbares und datenbasiertes Verständnis des Hamburger Straßennetzes zu entwickeln.

Dazu werden Geodaten mit SQL, PostgreSQL/PostGIS und Python verarbeitet und analysiert. Die Ergebnisse sollen anschließend in interaktiven Dashboards mit Streamlit und Power BI dargestellt werden.

Das Projekt verbindet Geodatenanalyse, Datenqualität, Datenaufbereitung und Business Intelligence in einem durchgängigen Analyseprozess.

## 2. Fachliche Fragestellungen

Das Projekt untersucht folgende Fragen:

- Wie viele Straßenabschnitte enthält der analysierte Datenbestand?
- Wie verteilt sich die gesamte Straßenlänge auf die vorhandenen Straßenklassen?
- Welche Straßenklassen dominieren hinsichtlich der Anzahl und der Gesamtlänge?
- Wie können räumliche Daten geprüft und für zuverlässige Analysen aufbereitet werden?
- Wie lassen sich die Ergebnisse verständlich und interaktiv visualisieren?

Eine spätere Erweiterung soll zusätzliche Verkehrsdaten einbeziehen, um weitere verkehrsbezogene Fragestellungen zu untersuchen.

## 3. Technischer Analyseprozess

### Datenverarbeitung und räumliche Analyse

Mit PostgreSQL und PostGIS werden Straßenobjekte räumlich analysiert und auf den untersuchten Hamburger Gebietsbereich bezogen.

### Datenaufbereitung mit Python

Python und Pandas werden verwendet, um Analyseergebnisse einzulesen, zusammenzufassen und für die Visualisierung aufzubereiten.

### Visualisierung

Die Ergebnisse werden zunächst mit Matplotlib visualisiert. Anschließend werden zwei ergänzende Darstellungsformen entwickelt:

- **Streamlit:** interaktives Analyse-Dashboard mit Python.
- **Power BI:** Business-Intelligence-Bericht mit Kennzahlen, Datenmodellierung und DAX-Measures.

## 4. Aktueller Datenstand

| Kennzahl | Ergebnis |
|---|---:|
| Analysierte Straßenabschnitte | 40.642 |
| Gesamte berechnete Straßenlänge | 5.156,25 km |
| Straßenklassen im aktuellen Bericht | 3 |
| Fehlende Werte in der Exportdatei | 0 |

### Verteilung nach Straßenklasse

| Klasse | Anzahl der Abschnitte | Gesamtlänge |
|---|---:|---:|
| G | 39.239 | 4.826,47 km |
| A | 618 | 182,77 km |
| B | 785 | 147,01 km |
| **Gesamt** | **40.642** | **5.156,25 km** |

## 5. Erste Analyseergebnisse

### Insight 1: Dominanz der Klasse G

Die Klasse G umfasst mit 4.826,47 km rund 93,60 % der gesamten im Bericht ausgewiesenen Straßenlänge.

### Insight 2: Unterschied zwischen Anzahl und Länge

Die Anzahl der Straßenabschnitte und ihre Gesamtlänge beschreiben unterschiedliche Eigenschaften des Straßennetzes. Deshalb werden beide Kennzahlen getrennt betrachtet.

### Insight 3: Datenqualität

Die exportierte Zusammenfassung enthält drei Straßenklassen und weist keine fehlenden Werte in den geprüften Spalten auf.

Diese Prüfung bestätigt die Vollständigkeit der CSV-Zusammenfassung, ersetzt jedoch keine vollständige Prüfung der räumlichen Datenqualität.

## 6. Aktuelle Visualisierungen

1. `road_network_by_class.png` – Gesamtlänge nach Straßenklasse.
2. `road_segments_by_class.png` – Anzahl der Straßenabschnitte nach Klasse.
3. `road_length_share_by_class.png` – Prozentualer Anteil der Straßenlänge nach Klasse.

Alle drei Grafiken werden mit einem gemeinsamen dunklen Design und goldfarbenen Akzenten erstellt.

## 7. Grenzen der bisherigen Analyse

Die bisherigen Ergebnisse beschreiben die Straßenstruktur anhand der verfügbaren Geodaten.

Aus diesen Kennzahlen allein lassen sich keine belastbaren Aussagen über Verkehrsaufkommen, Stau, Verkehrssicherheit oder die Qualität der Verkehrsanbindung ableiten.

Dafür werden zusätzliche, geeignete Daten und weiterführende Analysen benötigt.

Die Ergebnisse beziehen sich auf den aktuell verwendeten Datenbestand und die implementierte räumliche Abgrenzung.

## 8. Geplante nächste Schritte

1. Erstellung eines Management-Berichts in Markdown.
2. Aufbau eines interaktiven Streamlit-Dashboards.
3. Entwicklung eines Power-BI-Berichts mit Datenmodell und DAX-Kennzahlen.
4. Abgleich der Kennzahlen zwischen Python, Streamlit und Power BI.
5. Erweiterung um geeignete Verkehrsdaten und zusätzliche fachliche Analysen.
6. Dokumentation und Vorbereitung des Projekts für das Portfolio.

## 9. Angestrebte Kompetenzen

Durch dieses Projekt sollen praktische Fähigkeiten in folgenden Bereichen demonstriert werden:

- SQL und räumliche Datenanalyse mit PostgreSQL/PostGIS
- Datenaufbereitung und Datenprüfung mit Python und Pandas
- Datenvisualisierung mit Matplotlib
- Entwicklung interaktiver Anwendungen mit Streamlit
- Datenmodellierung, DAX und Reporting mit Power BI
- Fachliche Interpretation von Kennzahlen und transparente Dokumentation von Analysegrenzen

## 10. Zusammenfassung

Das Projekt entwickelt sich von einer räumlichen Analyse des Hamburger Straßennetzes zu einer durchgängigen Datenanalyse- und Business-Intelligence-Anwendung.

Der Schwerpunkt liegt auf nachvollziehbarer Datenverarbeitung, überprüfbaren Kennzahlen, verständlicher Visualisierung und der schrittweisen Erweiterung um weitere fachlich relevante Daten.


## Datenqualitätsanalyse: Geschwindigkeitsangaben

### Ziel
Untersuchung der Vollständigkeit der Geschwindigkeitsattribute im ursprünglichen Straßennetz-Datensatz und Vergleich der Ergebnisse nach Straßenklasse.

### Ergebnisse

| Straßenklasse | Anzahl Segmente | Fehlende Geschwindigkeitsangaben | Anteil fehlender Werte |
|---|---:|---:|---:|
| A | 659 | 144 | 21,85 % |
| B | 792 | 24 | 3,03 % |
| G | 39.310 | 8.635 | 21,97 % |
| **Gesamt** | **40.761** | **8.803** | **21,60 %** |

### Interpretation
Insgesamt fehlen bei 8.803 von 40.761 Straßensegmenten die Geschwindigkeitsangaben. Dies entspricht einem Anteil von 21,60 %.

Die Straßenklasse G weist mit 8.635 Segmenten die höchste absolute Anzahl fehlender Werte auf. In der Klasse A fehlen bei 21,85 % der Segmente die Geschwindigkeitsangaben. Die Klasse B weist mit 3,03 % den niedrigsten Anteil fehlender Werte auf.

Die Ergebnisse zeigen, dass die Vollständigkeit der Geschwindigkeitsattribute zwischen den Straßenklassen variiert.

### Methodik und Einschränkungen
Die Analyse wurde mit PostgreSQL durchgeführt. Fehlende Werte wurden über `NULLIF(BTRIM(geschwindigkeit::text), '') IS NULL` identifiziert. Dadurch werden sowohl NULL-Werte als auch leere oder ausschließlich aus Leerzeichen bestehende Einträge berücksichtigt.

Das Attribut `geschwindigkeit` enthält neben numerischen Angaben auch textuelle Beschreibungen, zeitabhängige Regelungen, variable Geschwindigkeitsangaben und kombinierte Werte. Deshalb wurden die Rohwerte zunächst kategorisiert, anstatt sie unmittelbar in numerische Geschwindigkeiten umzuwandeln.

Fehlende Angaben sind nicht automatisch fehlerhafte Daten. Aus dieser Analyse lässt sich außerdem keine abschließende Aussage über die rechtlich geltenden Geschwindigkeitsbegrenzungen ableiten.

**Datengrundlage:** `public.road_network` – ursprünglicher Datensatz mit 40.761 Segmenten. Die Ergebnisse beziehen sich nicht ausschließlich auf die auf das Hamburger Stadtgebiet zugeschnittene Netzansicht.


### Ergänzende Analyse: Straßennetz innerhalb der Hamburger Stadtgrenze

Für die auf das Hamburger Stadtgebiet zugeschnittene Netzansicht `analytics.v_road_network_hamburg` wurde die Vollständigkeit der Geschwindigkeitsangaben erneut untersucht.

| Straßenklasse | Anzahl Segmente | Fehlende Geschwindigkeitsangaben | Anteil fehlender Werte |
|---|---:|---:|---:|
| A | 618 | 105 | 16,99 % |
| B | 785 | 17 | 2,17 % |
| G | 39.239 | 8.575 | 21,85 % |
| **Gesamt** | **40.642** | **8.697** | **21,40 %** |

Im zugeschnittenen Hamburger Straßennetz fehlen bei 8.697 von 40.642 Segmenten die Geschwindigkeitsangaben. Dies entspricht 21,40 %.

Die Klasse G weist mit 8.575 Segmenten und einem Anteil von 21,85 % die meisten fehlenden Geschwindigkeitsangaben auf. In Klasse A beträgt der Anteil 16,99 %, während Klasse B mit 2,17 % den niedrigsten Anteil aufweist.

Die Analyse bezieht sich auf die räumlich zugeschnittene Netzansicht. Die Ergebnisse unterscheiden sich deshalb von der Analyse der ursprünglichen Tabelle `public.road_network`.



### Detailanalyse fehlender Straßenattribute

Bei 21 Segmenten der auf Hamburg zugeschnittenen Netzansicht fehlt die Angabe zur Straßenart (`wegeart`).

| Qualitätsindikator | Anzahl |
|---|---:|
| Segmente ohne Straßenart | 21 |
| Segmente ohne Straßennamen | 1 |
| Segmente ohne Wegenummer | 1 |
| Segmente ohne Geschwindigkeitsangabe | 19 |
| Segmente ohne Straßenname, Wegenummer und Geschwindigkeit gleichzeitig | 1 |

Bei 19 der 21 Segmente ohne Straßenart fehlt zusätzlich die Geschwindigkeitsangabe. Dies entspricht 90,48 % dieser Teilgruppe.

Die Ergebnisse zeigen, dass fehlende Attribute teilweise gemeinsam auftreten. Die Ursache der fehlenden Angaben lässt sich aus dieser Abfrage allein nicht bestimmen. Die betroffenen Datensätze wurden deshalb nicht verändert oder gelöscht, sondern als Ergebnis der Datenqualitätsanalyse dokumentiert.


