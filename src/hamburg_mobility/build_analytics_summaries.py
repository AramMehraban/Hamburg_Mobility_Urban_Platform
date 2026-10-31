
"""Build analytical summary CSV files from the validated road network export."""

from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
EXPORT_DIR = PROJECT_ROOT / "data" / "exports"
INPUT_FILE = EXPORT_DIR / "hamburg_road_network_analytics.csv"

EXPECTED_ROWS = 40761


def main() -> None:
    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Die Quelldatei wurde nicht gefunden: {INPUT_FILE}"
        )

    df = pd.read_csv(INPUT_FILE)

    if len(df) != EXPECTED_ROWS:
        raise ValueError(
            f"Erwartet: {EXPECTED_ROWS} Zeilen; gefunden: {len(df)}"
        )

    if df["feature_id"].isna().any():
        raise ValueError("feature_id enthält fehlende Werte.")

    if not df["feature_id"].is_unique:
        raise ValueError("feature_id ist nicht eindeutig.")

    required_columns = [
        "geometry_length_m",
        "road_class",
        "road_type",
        "speed_category",
        "speed_kmh_simple",
        "speed_raw",
        "speed_is_missing",
        "geometry_is_valid",
        "geometry_is_empty",
        "is_geometry_usable",
    ]

    missing_columns = [
        column for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Fehlende Pflichtspalten: {missing_columns}"
        )

    # 1. KPI summary
    simple_speeds = df["speed_kmh_simple"].dropna()

    kpi_rows = [
        ("total_road_segments", len(df), "segments"),
        ("unique_feature_ids", df["feature_id"].nunique(), "IDs"),
        (
            "sum_registered_segment_geometry_km",
            df["geometry_length_m"].sum() / 1000,
            "km",
        ),
        (
            "average_segment_geometry_length_m",
            df["geometry_length_m"].mean(),
            "m",
        ),
        (
            "median_segment_geometry_length_m",
            df["geometry_length_m"].median(),
            "m",
        ),
        (
            "segments_with_simple_numeric_speed",
            len(simple_speeds),
            "segments",
        ),
        (
            "simple_numeric_speed_median_kmh",
            simple_speeds.median(),
            "km/h",
        ),
        (
            "simple_numeric_speed_mean_kmh",
            simple_speeds.mean(),
            "km/h",
        ),
        (
            "segments_with_missing_speed",
            int(df["speed_is_missing"].sum()),
            "segments",
        ),
        (
            "invalid_geometries",
            int((~df["geometry_is_valid"].astype(bool)).sum()),
            "segments",
        ),
        (
            "empty_geometries",
            int(df["geometry_is_empty"].astype(bool).sum()),
            "segments",
        ),
        (
            "usable_geometries",
            int(df["is_geometry_usable"].astype(bool).sum()),
            "segments",
        ),
    ]

    kpi_summary = pd.DataFrame(
        kpi_rows,
        columns=["kpi", "value", "unit"],
    )
    kpi_summary["value"] = pd.to_numeric(
        kpi_summary["value"]
    ).round(2)

    # 2. Road class summary
    road_class_summary = (
        df.groupby("road_class", dropna=False)
        .agg(
            segment_count=("feature_id", "count"),
            sum_registered_segment_geometry_km=(
                "geometry_length_m",
                lambda values: values.sum() / 1000,
            ),
            average_segment_length_m=(
                "geometry_length_m", "mean"
            ),
        )
        .reset_index()
        .sort_values("segment_count", ascending=False)
    )

    road_class_summary[
        "share_percent"
    ] = (
        road_class_summary["segment_count"] / len(df) * 100
    ).round(2)

    road_class_summary[
        "sum_registered_segment_geometry_km"
    ] = road_class_summary[
        "sum_registered_segment_geometry_km"
    ].round(2)

    road_class_summary[
        "average_segment_length_m"
    ] = road_class_summary[
        "average_segment_length_m"
    ].round(2)

    # 3. Road type summary
    road_type_summary = (
        df.assign(
            road_type=df["road_type"].fillna("missing")
        )
        .groupby("road_type")
        .agg(
            segment_count=("feature_id", "count"),
        )
        .reset_index()
        .sort_values("segment_count", ascending=False)
    )

    road_type_summary["share_percent"] = (
        road_type_summary["segment_count"] / len(df) * 100
    ).round(2)

    # 4. Simple numeric speed summary
    speed_data = df.loc[
        df["speed_category"].eq("simple_numeric")
        & df["speed_kmh_simple"].notna(),
        "speed_kmh_simple",
    ]

    speed_summary = (
        speed_data.value_counts()
        .rename_axis("speed_kmh")
        .reset_index(name="segment_count")
        .sort_values("speed_kmh")
        .reset_index(drop=True)
    )

    speed_summary["share_of_simple_numeric_percent"] = (
        speed_summary["segment_count"] / len(speed_data) * 100
    ).round(2)

    # 5. Data quality summary
    quality_rows = []

    missing_columns_to_check = [
        "road_name",
        "road_type",
        "road_number",
        "street_code",
        "land_code",
        "district_code",
        "municipality_code",
        "speed_raw",
        "carriageway_count",
        "lanes_with_station",
        "lanes_against_station",
        "lanes_both_directions",
    ]

    for column in missing_columns_to_check:
        if column in df.columns:
            missing_count = int(df[column].isna().sum())
            quality_rows.append(
                {
                    "check_name": f"missing_values_{column}",
                    "result_count": missing_count,
                    "total_rows": len(df),
                    "result_percent": round(
                        missing_count / len(df) * 100, 2
                    ),
                    "status": (
                        "check_required"
                        if missing_count > 0
                        else "no_missing_values"
                    ),
                }
            )

    quality_checks = [
        (
            "invalid_geometries",
            int((~df["geometry_is_valid"].astype(bool)).sum()),
        ),
        (
            "empty_geometries",
            int(df["geometry_is_empty"].astype(bool).sum()),
        ),
        (
            "unusable_geometries",
            int((~df["is_geometry_usable"].astype(bool)).sum()),
        ),
        (
            "missing_speed_categories",
            int(df["speed_category"].isna().sum()),
        ),
        (
            "duplicate_feature_ids",
            int(df["feature_id"].duplicated().sum()),
        ),
    ]

    for check_name, count in quality_checks:
        quality_rows.append(
            {
                "check_name": check_name,
                "result_count": count,
                "total_rows": len(df),
                "result_percent": round(count / len(df) * 100, 2),
                "status": "check_required" if count else "passed",
            }
        )

    data_quality_summary = pd.DataFrame(quality_rows)

    # Save all five outputs
    outputs = {
        "kpi_summary.csv": kpi_summary,
        "road_class_summary.csv": road_class_summary,
        "road_type_summary.csv": road_type_summary,
        "speed_summary.csv": speed_summary,
        "data_quality_summary.csv": data_quality_summary,
    }

    for filename, table in outputs.items():
        output_path = EXPORT_DIR / filename
        table.to_csv(
            output_path,
            index=False,
            encoding="utf-8-sig",
        )
        print(f"Erstellt: {output_path.name} ({len(table)} Zeilen)")

    print("\nAlle fünf Analyse-Dateien wurden erstellt.")
    print(f"Quelle: {INPUT_FILE.name}")
    print("Die Quelldatei und die Datenbank wurden nicht verändert.")


if __name__ == "__main__":
    main()
