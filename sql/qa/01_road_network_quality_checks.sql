-- Hamburg Mobility & Urban Data Platform
-- Read-only data quality checks for public.road_network

SELECT
    COUNT(*) AS total_segments,
    COUNT(DISTINCT feature_id) AS unique_feature_ids,
    COUNT(*) - COUNT(DISTINCT feature_id) AS duplicate_id_count,
    COUNT(*) FILTER (
        WHERE geom IS NULL
    ) AS null_geometries,
    COUNT(*) FILTER (
        WHERE geom IS NOT NULL AND ST_IsEmpty(geom)
    ) AS empty_geometries,
    COUNT(*) FILTER (
        WHERE geom IS NOT NULL AND NOT ST_IsValid(geom)
    ) AS invalid_geometries,
    COUNT(*) FILTER (
        WHERE strassenname IS NULL OR BTRIM(strassenname) = ''
    ) AS missing_road_names,
    COUNT(*) FILTER (
        WHERE geschwindigkeit IS NULL OR BTRIM(geschwindigkeit) = ''
    ) AS missing_speed_information,
    COUNT(*) FILTER (
        WHERE wegeart IS NULL OR BTRIM(wegeart) = ''
    ) AS missing_road_types
FROM public.road_network;

-- Check geometry type and coordinate reference system.
SELECT
    ST_GeometryType(geom) AS geometry_type,
    ST_SRID(geom) AS srid,
    COUNT(*) AS feature_count
FROM public.road_network
GROUP BY ST_GeometryType(geom), ST_SRID(geom)
ORDER BY feature_count DESC;

-- Check indexes currently defined for the table.
SELECT
    indexname,
    indexdef
FROM pg_indexes
WHERE schemaname = 'public'
  AND tablename = 'road_network'
ORDER BY indexname;
