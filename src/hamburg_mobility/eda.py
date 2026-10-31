"""Exploratory data analysis for the Hamburg road network Parquet file."""

from pathlib import Path
import json

import geopandas as gpd
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_FILE = PROJECT_ROOT / "data" / "processed" / "hamburg_road_network_utm32.parquet"
EXPORT_DIR = PROJECT_ROOT / "data" / "exports"


def main() -> None:
    if not DATA_FILE.is_file():
        raise FileNotFoundError(f"Processed Parquet file not found: {DATA_FILE}")

    EXPORT_DIR.mkdir(parents=True, exist_ok=True)

    roads = gpd.read_parquet(DATA_FILE)

    missing_values = roads.isna().sum().sort_values(ascending=False)
    missing_report = (
        missing_values.rename_axis("column")
        .reset_index(name="missing_count")
    )
    missing_report["missing_percent"] = (
        missing_report["missing_count"] / len(roads) * 100
    ).round(2)
    missing_report.to_csv(
        EXPORT_DIR / "eda_missing_values.csv",
        index=False,
        encoding="utf-8-sig",
    )

    categorical_reports = []
    for column in ("klasse", "wegeart", "geschwindigkeit"):
        if column in roads.columns:
            counts = (
                roads[column]
                .fillna("(NULL)")
                .astype(str)
                .value_counts(dropna=False)
                .rename_axis("value")
                .reset_index(name="record_count")
            )
            counts.insert(0, "column", column)
            categorical_reports.append(counts)

    if categorical_reports:
        pd.concat(categorical_reports, ignore_index=True).to_csv(
            EXPORT_DIR / "eda_categorical_distributions.csv",
            index=False,
            encoding="utf-8-sig",
        )

    geometry = roads.geometry
    summary = {
        "source_file": str(DATA_FILE.relative_to(PROJECT_ROOT)),
        "row_count": int(len(roads)),
        "column_count": int(len(roads.columns)),
        "columns": list(roads.columns),
        "crs": str(roads.crs) if roads.crs else None,
        "feature_id_exists": "feature_id" in roads.columns,
        "feature_id_null_count": (
            int(roads["feature_id"].isna().sum())
            if "feature_id" in roads.columns else None
        ),
        "feature_id_unique": (
            bool(roads["feature_id"].is_unique)
            if "feature_id" in roads.columns else None
        ),
        "geometry_null_count": int(geometry.isna().sum()),
        "geometry_empty_count": int(geometry.is_empty.sum()),
        "geometry_invalid_count": int((~geometry.is_valid).sum()),
        "geometry_types": {
            str(key): int(value)
            for key, value in geometry.geom_type.value_counts(dropna=False).items()
        },
        "missing_values_total": int(roads.isna().sum().sum()),
    }

    with (EXPORT_DIR / "eda_summary.json").open("w", encoding="utf-8") as file:
        json.dump(summary, file, ensure_ascii=False, indent=2)

    print("EDA completed successfully.")
    print(f"Rows: {summary['row_count']:,}")
    print(f"Columns: {summary['column_count']}")
    print(f"CRS: {summary['crs']}")
    print(f"Null geometries: {summary['geometry_null_count']}")
    print(f"Empty geometries: {summary['geometry_empty_count']}")
    print(f"Invalid geometries: {summary['geometry_invalid_count']}")
    print(f"Reports saved to: {EXPORT_DIR}")


if __name__ == "__main__":
    main()
