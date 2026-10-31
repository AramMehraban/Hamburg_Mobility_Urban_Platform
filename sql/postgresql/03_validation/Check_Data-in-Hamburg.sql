WITH boundary AS (
    SELECT boundary_geom AS geom
    FROM analytics.hamburg_boundary_check
    WHERE id = 1
)
SELECT
    CASE
        WHEN ST_CoveredBy(r.geom, b.geom)
            THEN 'entirely_inside'
        WHEN NOT ST_Intersects(r.geom, b.geom)
            THEN 'entirely_outside'
        ELSE 'partly_inside_or_touches_boundary'
    END AS location_class,

    COUNT(*) AS segments,

    ROUND(
        (SUM(ST_Length(r.geom)) / 1000.0)::numeric,
        2
    ) AS total_segment_length_km

FROM public.road_network AS r
CROSS JOIN boundary AS b

GROUP BY 1
ORDER BY 1;


-- Identify Road Segments Outside Hamburg 
SELECT
    r.feature_id,
    r.klasse,
    r.wegenummer,
    r.strassenname,
    r.wegeart,
    ROUND(
        (ST_Length(r.geom) / 1000.0)::numeric,
        3
    ) AS length_km
FROM public.road_network AS r
CROSS JOIN analytics.hamburg_boundary_check AS b
WHERE b.id = 1
  AND NOT ST_Intersects(r.geom, b.boundary_geom)
ORDER BY ST_Length(r.geom) DESC
LIMIT 30;

-- Analyze Road Segments Intersecting the Hamburg Boundary
WITH boundary AS (
    SELECT boundary_geom AS geom
    FROM analytics.hamburg_boundary_check
    WHERE id = 1
)
SELECT
    CASE
        WHEN ST_Touches(r.geom, b.geom)
            THEN 'touches_only'
        WHEN ST_Crosses(r.geom, b.geom)
            THEN 'crosses_boundary'
        WHEN ST_CoveredBy(r.geom, b.geom)
            THEN 'covered_by_boundary'
        ELSE 'other_intersection'
    END AS intersection_type,
    COUNT(*) AS segments,
    ROUND(
        (SUM(ST_Length(r.geom)) / 1000.0)::numeric,
        2
    ) AS total_full_segment_length_km
FROM public.road_network AS r
CROSS JOIN boundary AS b
WHERE ST_Intersects(r.geom, b.geom)
  AND NOT ST_CoveredBy(r.geom, b.geom)
GROUP BY 1
ORDER BY 1;


-- Calculate Road Length Within Hamburg for Boundary-Crossing Segments
WITH boundary AS (
    SELECT boundary_geom AS geom
    FROM analytics.hamburg_boundary_check
    WHERE id = 1
),
road_parts AS (
    SELECT
        r.feature_id,
        ST_Length(r.geom) AS full_length_m,
        ST_Intersection(r.geom, b.geom) AS inside_geom
    FROM public.road_network AS r
    CROSS JOIN boundary AS b
    WHERE ST_Crosses(r.geom, b.geom)
)
SELECT
    COUNT(*) AS crossing_segments,
    ROUND(
        (SUM(full_length_m) / 1000.0)::numeric,
        2
    ) AS full_length_km,
    ROUND(
        (
            SUM(ST_Length(inside_geom))
            / 1000.0
        )::numeric,
        2
    ) AS length_inside_hamburg_km,
    ROUND(
        (
            SUM(full_length_m - ST_Length(inside_geom))
            / 1000.0
        )::numeric,
        2
    ) AS length_outside_hamburg_km
FROM road_parts;
