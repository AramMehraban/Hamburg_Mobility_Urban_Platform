
"""Export an analysis-ready CSV from the Hamburg road network PostGIS table."""

import sys
from getpass import getpass
from pathlib import Path

import pandas as pd
from sqlalchemy import text

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from config.database import create_database_engine


PROJECT_ROOT = Path(__file__).resolve().parents[2]
EXPORT_DIR = PROJECT_ROOT / "data" / "exports"
OUTPUT_FILE = EXPORT_DIR / "hamburg_road_network_analytics.csv"
EXPECTED_ROWS = 40761
EXPECTED_COLUMNS = 34

SIMPLE_SPEED_PATTERN = (
    r"^[0-9]+([.,][0-9]+)?[[:space:]]*km/h$"
)

QUERY = """
SELECT
    feature_id,
    strassenname AS road_name,
    klasse AS road_class,
    wegeart AS road_type,
    wegenummer AS road_number,
    strassenschluessel AS street_code,
    landesschluessel AS land_code,
    kreisschluessel AS district_code,
    gemeindeschluessel AS municipality_code,

    ST_Length(geom)::double precision AS geometry_length_m,
    ST_X(ST_Transform(ST_Centroid(geom), 4326))
        AS centroid_longitude,
    ST_Y(ST_Transform(ST_Centroid(geom), 4326))
        AS centroid_latitude,
    ST_SRID(geom) AS geometry_srid,

    geschwindigkeit AS speed_raw,

    CASE
        WHEN geschwindigkeit IS NULL
             OR BTRIM(geschwindigkeit) = ''
            THEN 'missing'
        WHEN geschwindigkeit ~ '^[0-9]+([.,][0-9]+)?[[:space:]]*km/h$'
            THEN 'simple_numeric'
        WHEN geschwindigkeit LIKE '%|%'
            THEN 'multiple_entries'
        WHEN geschwindigkeit ~*
             '(werktags|mo-fr|mo–fr|lärmschutz|22[[:space:]]*-[[:space:]]*6|6[[:space:]]*-[[:space:]]*22|sonst)'
            THEN 'conditional'
        WHEN geschwindigkeit ~ '[0-9]+[[:space:]]*-[[:space:]]*[0-9]+'
            THEN 'contains_number_or_range'
        ELSE 'descriptive_non_numeric'
    END AS speed_category,

    CASE
        WHEN geschwindigkeit ~
             '^[0-9]+([.,][0-9]+)?[[:space:]]*km/h$'
        THEN REPLACE(
            REGEXP_REPLACE(
                geschwindigkeit,
                '[[:space:]]*km/h$',
                '',
                'i'
            ),
            ',',
            '.'
        )::double precision
        ELSE NULL
    END AS speed_kmh_simple,

    (
        geschwindigkeit IS NULL
        OR BTRIM(geschwindigkeit) = ''
    ) AS speed_is_missing,

    COALESCE(
        geschwindigkeit ~*
        '(werktags|mo-fr|mo–fr|lärmschutz|sonst)'
        OR geschwindigkeit ~*
        '[0-9]+[[:space:]]*-[[:space:]]*[0-9]+.*h',
        FALSE
    ) AS speed_has_condition,

    COALESCE(
        geschwindigkeit LIKE '%|%',
        FALSE
    ) AS speed_has_multiple_entries,

    bahnigkeit AS carriageway_count,
    fahrstreifenanzahl_in_stationierungsrichtung
        AS lanes_with_station,
    fahrstreifenanzahl_gegen_stationierungsrichtung
        AS lanes_against_station,
    fahrstreifenanzahl_in_beide_richtungen
        AS lanes_both_directions,

    (
        strassenname IS NOT NULL
        AND BTRIM(strassenname) <> ''
    ) AS has_road_name,

    (
        wegeart IS NOT NULL
        AND BTRIM(wegeart) <> ''
    ) AS has_road_type,

    ST_IsValid(geom) AS geometry_is_valid,
    ST_IsEmpty(geom) AS geometry_is_empty,

    (
        landesschluessel IS NULL
        OR kreisschluessel IS NULL
        OR gemeindeschluessel IS NULL
    ) AS has_missing_geo_code,

    1 AS segment_count,
    (klasse = 'A') AS is_class_a,
    (klasse = 'B') AS is_class_b,
    (klasse = 'G') AS is_class_g,

    COALESCE(
        geschwindigkeit ~
        '^[0-9]+([.,][0-9]+)?[[:space:]]*km/h$',
        FALSE
    ) AS is_speed_simple_numeric,

    (
        geom IS NOT NULL
        AND NOT ST_IsEmpty(geom)
        AND ST_IsValid(geom)
    ) AS is_geometry_usable

FROM public.road_network
ORDER BY feature_id;
"""


def main() -> None:
    username = "postgres"
    password = getpass(
        "Passwort für den PostgreSQL-Benutzer postgres: "
    )

    engine = create_database_engine(username, password)

    try:
        with engine.connect() as connection:
            current_db = connection.execute(
                text("SELECT current_database()")
            ).scalar_one()

            if current_db != "hamburg_mobility_urban_new":
                raise RuntimeError(
                    f"Unerwartete Datenbank: {current_db}"
                )

            roads = pd.read_sql_query(text(QUERY), connection)

        if len(roads) != EXPECTED_ROWS:
            raise ValueError(
                f"Erwartet {EXPECTED_ROWS} Zeilen, "
                f"gefunden: {len(roads)}"
            )

        if roads.columns.size != EXPECTED_COLUMNS:
            raise ValueError(
                f"Erwartet {EXPECTED_COLUMNS} Spalten, "
                f"gefunden: {roads.columns.size}"
            )

        if roads["feature_id"].isna().any():
            raise ValueError("feature_id enthält NULL-Werte.")

        if not roads["feature_id"].is_unique:
            raise ValueError("feature_id ist nicht eindeutig.")

        required_columns = [
            "geometry_length_m",
            "centroid_longitude",
            "centroid_latitude",
        ]

        for column in required_columns:
            if roads[column].isna().any():
                raise ValueError(
                    f"Fehlende Werte in {column} gefunden."
                )

        if not roads["geometry_srid"].eq(25832).all():
            raise ValueError(
                "Nicht alle Geometrien haben SRID 25832."
            )

        flag_columns = [
            "speed_is_missing",
            "speed_has_condition",
            "speed_has_multiple_entries",
            "is_speed_simple_numeric",
        ]

        for column in flag_columns:
            if roads[column].isna().any():
                raise ValueError(
                    f"NULL-Werte im Flag {column} gefunden."
                )

        if roads["speed_category"].isna().any():
            raise ValueError(
                "Nicht klassifizierte Geschwindigkeitswerte gefunden."
            )

        EXPORT_DIR.mkdir(parents=True, exist_ok=True)
        roads.to_csv(
            OUTPUT_FILE,
            index=False,
            encoding="utf-8-sig",
        )

        print("CSV-Export erfolgreich.")
        print(f"Zeilen: {len(roads):,}")
        print(f"Spalten: {len(roads.columns)}")
        print(
            "Eindeutige feature_id: "
            f"{roads['feature_id'].nunique():,}"
        )
        print("Geschwindigkeitskategorien:")
        print(roads["speed_category"].value_counts().to_string())
        print("NULL-Prüfung der Geschwindigkeits-Flags:")
        for column in flag_columns:
            print(f"  {column}: {roads[column].isna().sum()}")
        print(f"Datei: {OUTPUT_FILE}")
        print("Die Quelltabelle wurde nicht verändert.")

    finally:
        engine.dispose()


if __name__ == "__main__":
    main()
