CREATE SCHEMA IF NOT EXISTS analytics;

CREATE OR REPLACE VIEW analytics.v_road_network_overview AS
SELECT
    COUNT(*) AS total_road_segments,
    COUNT(DISTINCT feature_id) AS unique_segments,
    SUM(abschnittslaenge) AS total_segment_length,
    ROUND(AVG(abschnittslaenge)::numeric, 2) AS avg_segment_length,
    COUNT(*) FILTER (
        WHERE geschwindigkeit IS NULL OR BTRIM(geschwindigkeit) = ''
    ) AS missing_speed_information,
    COUNT(*) FILTER (
        WHERE strassenname IS NULL OR BTRIM(strassenname) = ''
    ) AS missing_road_names,
    COUNT(*) FILTER (
        WHERE wegeart IS NULL OR BTRIM(wegeart) = ''
    ) AS missing_road_types,
    COUNT(*) FILTER (
        WHERE geom IS NULL OR ST_IsEmpty(geom)
    ) AS missing_or_empty_geometries,
    ST_SRID(ST_Collect(geom)) AS srid
FROM public.road_network;

CREATE OR REPLACE VIEW analytics.v_road_network_by_type AS
SELECT
    klasse,
    wegeart,
    COUNT(*) AS segment_count,
    SUM(abschnittslaenge) AS total_segment_length,
    ROUND(AVG(abschnittslaenge)::numeric, 2) AS avg_segment_length
FROM public.road_network
GROUP BY klasse, wegeart;
