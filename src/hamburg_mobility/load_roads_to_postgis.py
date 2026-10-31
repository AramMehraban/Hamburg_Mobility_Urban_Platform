from getpass import getpass
from pathlib import Path

import geopandas as gpd
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL


PROJECT_ROOT = Path(__file__).resolve().parents[2]
PARQUET_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "hamburg_road_network_utm32.parquet"
)

DATABASE_NAME = "hamburg_mobility_urban_new"
EXPECTED_ROWS = 40761
TARGET_CRS = "EPSG:25832"

INTEGER_COLUMNS = [
    "von_station",
    "bis_station",
    "landesschluessel",
    "kreisschluessel",
    "gemeindeschluessel",
    "abschnittslaenge",
    "ast",
    "fahrstreifenanzahl_in_stationierungsrichtung",
    "fahrstreifenanzahl_in_beide_richtungen",
    "fahrstreifenanzahl_gegen_stationierungsrichtung",
    "bahnigkeit",
]

TEXT_COLUMNS = [
    "von_netzknoten",
    "nach_netzknoten",
    "klasse",
    "wegenummer",
    "strassenname",
    "geschwindigkeit",
    "wegeart",
    "strassenschluessel",
    "europastrasse",
]

REQUIRED_COLUMNS = [
    "feature_id",
    *TEXT_COLUMNS[:5],
    "von_station",
    "bis_station",
    "landesschluessel",
    "kreisschluessel",
    "gemeindeschluessel",
    "abschnittslaenge",
    "ast",
    "fahrstreifenanzahl_in_stationierungsrichtung",
    "fahrstreifenanzahl_in_beide_richtungen",
    "fahrstreifenanzahl_gegen_stationierungsrichtung",
    "bahnigkeit",
    "geschwindigkeit",
    "wegeart",
    "strassenschluessel",
    "europastrasse",
    "geometry",
]


def main():
    if not PARQUET_PATH.is_file():
        raise FileNotFoundError(f"Parquet-Datei nicht gefunden: {PARQUET_PATH}")

    print("Lese Parquet-Datei ...")
    gdf = gpd.read_parquet(PARQUET_PATH)

    missing_columns = sorted(set(REQUIRED_COLUMNS) - set(gdf.columns))
    if missing_columns:
        raise ValueError(f"Fehlende Spalten: {missing_columns}")

    if len(gdf) != EXPECTED_ROWS:
        raise ValueError(
            f"Unerwartete Zeilenanzahl: {len(gdf)}; "
            f"erwartet: {EXPECTED_ROWS}"
        )

    if gdf["feature_id"].isna().any():
        raise ValueError("feature_id enthält NULL-Werte.")

    if not gdf["feature_id"].is_unique:
        raise ValueError("feature_id ist nicht eindeutig.")

    if gdf.crs is None or gdf.crs.to_epsg() != 25832:
        raise ValueError(f"Unerwartetes CRS: {gdf.crs}")

    if gdf.geometry.isna().any():
        raise ValueError("Geometrien enthalten NULL-Werte.")

    if gdf.geometry.is_empty.any():
        raise ValueError("Leere Geometrien gefunden.")

    if not gdf.geometry.is_valid.all():
        raise ValueError("Ungültige Geometrien gefunden.")

    if not gdf.geom_type.eq("LineString").all():
        raise ValueError("Es wurden Geometrietypen außer LineString gefunden.")

    print(f"Vorprüfung erfolgreich: {len(gdf)} Datensätze")
    print(f"CRS: {gdf.crs}")

        # Numerische Werte als echte Python-Integer oder None vorbereiten.
    for column in INTEGER_COLUMNS:
        values = pd.to_numeric(gdf[column], errors="raise")

        non_null = values.dropna()
        if not (non_null == non_null.round()).all():
            raise ValueError(f"Nicht-ganzzahlige Werte in {column}")

        gdf[column] = pd.Series(
            [
                int(value) if pd.notna(value) else None
                for value in values
            ],
            index=gdf.index,
            dtype=object,
        )

    # Fehlende Textwerte als SQL NULL behandeln.
    for column in TEXT_COLUMNS:
        gdf[column] = gdf[column].map(
            lambda value: None if pd.isna(value) else str(value)
        )

    gdf = gdf.rename_geometry("geom")

    password = getpass("Passwort für PostgreSQL-Benutzer postgres: ")

    url = URL.create(
        drivername="postgresql+psycopg",
        username="postgres",
        password=password,
        host="localhost",
        port=5432,
        database=DATABASE_NAME,
    )

    engine = create_engine(url)

    try:
        with engine.begin() as connection:
            current_db = connection.execute(
                text("SELECT current_database()")
            ).scalar_one()

            if current_db != DATABASE_NAME:
                raise RuntimeError(
                    f"Falsche Datenbank verbunden: {current_db}"
                )

            count = connection.execute(
                text("SELECT COUNT(*) FROM public.road_network")
            ).scalar_one()

            if count != 0:
                raise RuntimeError(
                    "Zieltabelle ist nicht leer. "
                    "Es wurden keine Daten eingefügt."
                )

            print("Zieltabellenprüfung erfolgreich: 0 Datensätze")
            print("Starte Übertragung nach PostgreSQL/PostGIS ...")

            gdf.to_postgis(
                name="road_network",
                con=connection,
                schema="public",
                if_exists="append",
                index=False,
                chunksize=1000,
            )

            inserted = connection.execute(
                text("SELECT COUNT(*) FROM public.road_network")
            ).scalar_one()

            if inserted != EXPECTED_ROWS:
                raise RuntimeError(
                    f"Anzahl nach dem Laden stimmt nicht: {inserted}"
                )

            unique_ids = connection.execute(
                text(
                    "SELECT COUNT(DISTINCT feature_id) "
                    "FROM public.road_network"
                )
            ).scalar_one()

            if unique_ids != EXPECTED_ROWS:
                raise RuntimeError(
                    f"Unerwartete Anzahl eindeutiger IDs: {unique_ids}"
                )

        print("Übertragung erfolgreich abgeschlossen.")
        print(f"Datenbank: {DATABASE_NAME}")
        print(f"Datensätze: {EXPECTED_ROWS}")
        print("Geometrie: LineString, EPSG:25832")

    finally:
        engine.dispose()


if __name__ == "__main__":
    main()
