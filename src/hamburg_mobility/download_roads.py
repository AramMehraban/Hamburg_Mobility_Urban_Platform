
from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

import geopandas as gpd
import requests


PROJECT_ROOT = Path(__file__).resolve().parents[2]

API_URL = (
    "https://api.hamburg.de/datasets/v1/"
    "strassen_und_wegenetz/collections/"
    "strassennetz_gesamt/items"
)

TARGET_CRS = "EPSG:25832"
TARGET_CRS_URI = "http://www.opengis.net/def/crs/EPSG/0/25832"
PAGE_SIZE = 1000
TIMEOUT_SECONDS = 60

OUTPUT_DIR = PROJECT_ROOT / "data" / "processed"
PARQUET_OUTPUT = OUTPUT_DIR / "hamburg_road_network_utm32.parquet"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger(__name__)


def fetch_features() -> list[dict[str, Any]]:
    """Download all road features in EPSG:25832."""
    features: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    offset = 0
    expected_count: int | None = None

    with requests.Session() as session:
        session.headers.update(
            {"Accept": "application/geo+json, application/json"}
        )

        while True:
            params = {
                "f": "json",
                "limit": PAGE_SIZE,
                "offset": offset,
                "crs": TARGET_CRS_URI,
            }

            response = session.get(
                API_URL,
                params=params,
                timeout=TIMEOUT_SECONDS,
            )
            response.raise_for_status()
            payload = response.json()

            if expected_count is None:
                expected_count = int(payload["numberMatched"])
                logger.info("API reports %s features.", expected_count)

            page = payload.get("features", [])
            if not page:
                break

            for feature in page:
                feature_id = feature.get("id")

                if feature_id is None:
                    raise ValueError("Feature without an ID detected.")

                key = str(feature_id)

                if key in seen_ids:
                    raise ValueError(f"Duplicate feature ID: {key}")

                seen_ids.add(key)
                features.append(feature)

            logger.info(
                "Downloaded %s / %s features.",
                len(features),
                expected_count,
            )

            offset += len(page)

            if len(features) >= expected_count:
                break

    if expected_count is None:
        raise RuntimeError("The API did not return numberMatched.")

    if len(features) != expected_count:
        raise RuntimeError(
            f"Expected {expected_count} features, got {len(features)}."
        )

    logger.info("Feature count and unique IDs validated.")
    return features


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    features = fetch_features()

    gdf = gpd.GeoDataFrame.from_features(
        features,
        crs=TARGET_CRS,
    )

    # Preserve the official API feature IDs as a regular column.
    gdf["feature_id"] = [
        feature["id"] for feature in features
    ]

    if gdf.empty:
        raise RuntimeError("The downloaded GeoDataFrame is empty.")

    if gdf.crs is None or gdf.crs.to_epsg() != 25832:
        raise RuntimeError(f"Unexpected CRS: {gdf.crs}")

    if gdf.geometry.isna().any():
        raise RuntimeError("Missing geometries detected.")

    if gdf.geometry.is_empty.any():
        raise RuntimeError("Empty geometries detected.")

    if not gdf.geometry.is_valid.all():
        raise RuntimeError("Invalid geometries detected.")

    # Write to a temporary file first.
    # Replace the final output only after validation succeeds.
    temporary_output = PARQUET_OUTPUT.with_name(
        PARQUET_OUTPUT.stem + ".tmp.parquet"
    )

    try:
        gdf.to_parquet(temporary_output, index=False)

        check = gpd.read_parquet(temporary_output)

        if len(check) != len(gdf):
            raise RuntimeError("Parquet row-count validation failed.")

        if check["feature_id"].nunique() != len(check):
            raise RuntimeError(
                "Duplicate feature IDs found in Parquet output."
            )

        if check.crs is None or check.crs.to_epsg() != 25832:
            raise RuntimeError("Parquet CRS validation failed.")

        if check.geometry.isna().any():
            raise RuntimeError(
                "Missing geometries found after Parquet read-back."
            )

        if check.geometry.is_empty.any():
            raise RuntimeError(
                "Empty geometries found after Parquet read-back."
            )

        if not check.geometry.is_valid.all():
            raise RuntimeError(
                "Invalid geometry found after Parquet read-back."
            )

        temporary_output.replace(PARQUET_OUTPUT)

    finally:
        if temporary_output.exists():
            temporary_output.unlink()

    logger.info("Processing completed successfully.")
    logger.info("Features: %s", len(check))
    logger.info("CRS: %s", check.crs)
    logger.info("Parquet: %s", PARQUET_OUTPUT)


if __name__ == "__main__":
    main()
