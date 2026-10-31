-- Create view

CREATE OR REPLACE VIEW analytics.v_road_network_hamburg AS
SELECT
    r.feature_id,
    r.klasse,
    r.wegenummer,
    r.strassenname,
    r.wegeart,
    r.geschwindigkeit,
    ST_Length(
        ST_Intersection(r.geom, b.boundary_geom)
    ) AS length_inside_m,
    ST_Intersection(
        r.geom,
        b.boundary_geom
    ) AS geom
FROM public.road_network AS r
CROSS JOIN analytics.hamburg_boundary_check AS b
WHERE b.id = 1
  AND ST_Intersects(r.geom, b.boundary_geom);


-- show segment coiunt
  SELECT
    COUNT(*) AS segment_count,
    ROUND(
        (SUM(length_inside_m) / 1000.0)::numeric,
        2
    ) AS total_length_km,
    ROUND(
        (AVG(length_inside_m))::numeric,
        2
    ) AS average_segment_length_m
FROM analytics.v_road_network_hamburg;

-- check view result 
SELECT
    feature_id,
    klasse,
    strassenname,
    wegeart,
    ROUND(length_inside_m::numeric, 2) AS length_inside_m
FROM analytics.v_road_network_hamburg
ORDER BY length_inside_m DESC
LIMIT 10;


-- Check Road Type
SELECT
    klasse,
    COUNT(*) AS segment_count,
    ROUND(
        (SUM(length_inside_m) / 1000.0)::numeric,
        2
    ) AS total_length_km
FROM analytics.v_road_network_hamburg
GROUP BY klasse
ORDER BY total_length_km DESC;

