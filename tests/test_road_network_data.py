from pathlib import Path

import geopandas as gpd
import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = PROJECT_ROOT / "data" / "processed" / "hamburg_road_network_utm32.parquet"
EXPECTED_ROWS = 40761


@pytest.fixture(scope="module")
def roads():
    if not DATA_FILE.exists():
        pytest.fail(f"Processed data file not found: {DATA_FILE}")

    return gpd.read_parquet(DATA_FILE)


def test_processed_file_exists():
    assert DATA_FILE.is_file()


def test_expected_row_count(roads):
    assert len(roads) == EXPECTED_ROWS


def test_feature_ids_are_present_and_unique(roads):
    assert "feature_id" in roads.columns
    assert roads["feature_id"].notna().all()
    assert roads["feature_id"].is_unique


def test_coordinate_reference_system(roads):
    assert roads.crs is not None
    assert roads.crs.to_epsg() == 25832


def test_geometries_are_present(roads):
    assert roads.geometry.notna().all()
    assert (~roads.geometry.is_empty).all()


def test_geometries_are_valid(roads):
    assert roads.geometry.is_valid.all()


def test_all_geometries_are_linestrings(roads):
    assert roads.geometry.geom_type.eq("LineString").all()


def test_required_columns_exist(roads):
    required = {
        "feature_id",
        "strassenname",
        "klasse",
        "wegeart",
        "geschwindigkeit",
    }
    assert required.issubset(set(roads.columns))
