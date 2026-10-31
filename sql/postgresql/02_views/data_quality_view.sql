SELECT
    klasse,
    COUNT(*) AS total_segments,

    COUNT(*) FILTER (
        WHERE NULLIF(
            BTRIM(geschwindigkeit::text), ''
        ) IS NULL
    ) AS missing_speed,

    ROUND(
        100.0 * COUNT(*) FILTER (
            WHERE NULLIF(
                BTRIM(geschwindigkeit::text), ''
            ) IS NULL
        ) / NULLIF(COUNT(*), 0),
        2
    ) AS missing_speed_percent

FROM analytics.v_road_network_hamburg
GROUP BY klasse
ORDER BY klasse;

-- Create Data Quality view
CREATE OR REPLACE VIEW analytics.v_road_network_data_quality AS
SELECT
    klasse,
    COUNT(*) AS total_segments,

    COUNT(*) FILTER (
        WHERE NULLIF(
            BTRIM(geschwindigkeit::text), ''
        ) IS NULL
    ) AS missing_speed,

    ROUND(
        100.0 * COUNT(*) FILTER (
            WHERE NULLIF(
                BTRIM(geschwindigkeit::text), ''
            ) IS NULL
        ) / NULLIF(COUNT(*), 0),
        2
    ) AS missing_speed_percent,

    COUNT(*) FILTER (
        WHERE NULLIF(
            BTRIM(wegeart::text), ''
        ) IS NULL
    ) AS missing_road_type

FROM analytics.v_road_network_hamburg
GROUP BY klasse;


-- show Data from analytics.v_road_network_data_quality
SELECT *
FROM analytics.v_road_network_data_quality
ORDER BY klasse;

