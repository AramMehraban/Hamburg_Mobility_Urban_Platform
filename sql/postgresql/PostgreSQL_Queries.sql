
-- Show Database
SELECT
    current_database() AS database_name,
    PostGIS_Version() AS postgis_version,
    COUNT(*) AS road_segments
FROM public.road_network;


-- Show Schema
SELECT
    schema_name
FROM information_schema.schemata
WHERE schema_name = 'analytics';

SELECT
    table_name
FROM information_schema.tables
WHERE table_schema = 'analytics'
ORDER BY table_name;

-- Validate Hamburg Boundary Geometry
SELECT
    ST_SRID(boundary_geom) AS srid,
    ST_GeometryType(boundary_geom) AS geometry_type,
    ST_IsValid(boundary_geom) AS is_valid,
    COUNT(*) AS boundary_rows
FROM analytics.hamburg_boundary_check
GROUP BY
    ST_SRID(boundary_geom),
    ST_GeometryType(boundary_geom),
    ST_IsValid(boundary_geom);


-- Create Grenze Table
CREATE TABLE analytics.hamburg_boundary_check (
    id integer PRIMARY KEY,
    boundary_geom geometry(MultiPolygon, 25832) NOT NULL
);


-- show Table
SELECT
    COUNT(*) AS boundary_rows
FROM analytics.hamburg_boundary_check;

-- EPSG:4326 to EPSG:25832
SELECT
    ST_AsText(
        ST_Transform(
            ST_SetSRID(
                ST_GeomFromText('POINT(10.0 53.5)'),
                4326
            ),
            25832
        )
    ) AS transformed_point;
	

-- Read Geometrie from GeoJSON File 
INSERT INTO analytics.hamburg_boundary_check (id, boundary_geom)
VALUES (
    1,
    ST_Multi(
        ST_Transform(
            ST_SetSRID(
                ST_GeomFromGeoJSON(
                    (
                        SELECT ST_AsGeoJSON(geom)
                        FROM (
                            SELECT ST_GeomFromGeoJSON(
                                (feature->'geometry')::text
                            ) AS geom
                            FROM (
                                SELECT jsonb_array_elements(
                                    pg_read_file(
                                        'C:/Users/Kunde/Documents/Project-zum-Lebenslauf/GitHub_Projects/Hamburg_Mobility_Urban_Platform_New/data/raw/ALKIS-Verwaltungsgrenze-Hamburg/app_landesgrenze_EPSG_4326.json'
                                )::jsonb->'features'
                                ) AS feature
                            ) AS f
                        ) AS g
                    )
                ),
                4326
            ),
            25832
        )
    )
);


-- Read Username and Password in aktuall Database 
SELECT
    current_user,
    current_database(),
    has_table_privilege(
        current_user,
        'analytics.hamburg_boundary_check',
        'INSERT'
    ) AS can_insert_boundary;


-- Read all Rows from boundary_rows File
SELECT
    COUNT(*) AS boundary_rows,
    COALESCE(
        SUM(ST_SRID(boundary_geom)),
        0
    ) AS srid_sum
FROM analytics.hamburg_boundary_check;


