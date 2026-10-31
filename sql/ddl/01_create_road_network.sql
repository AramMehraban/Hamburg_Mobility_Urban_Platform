-- DDL: Road network table
-- Database: hamburg_mobility_urban_new
-- Purpose: Document the table structure for a future clean setup.
-- WARNING: Review before execution. Do not run against the existing database
-- without checking whether the target table already exists.

CREATE TABLE public.road_network (
    feature_id BIGINT NOT NULL,
    von_netzknoten TEXT,
    nach_netzknoten TEXT,
    von_station BIGINT,
    bis_station BIGINT,
    klasse TEXT,
    wegenummer TEXT,
    strassenname TEXT,
    landesschluessel SMALLINT,
    kreisschluessel SMALLINT,
    gemeindeschluessel INTEGER,
    abschnittslaenge BIGINT,
    ast SMALLINT,
    fahrstreifenanzahl_in_stationierungsrichtung SMALLINT,
    fahrstreifenanzahl_in_beide_richtungen SMALLINT,
    fahrstreifenanzahl_gegen_stationierungsrichtung SMALLINT,
    bahnigkeit SMALLINT,
    geschwindigkeit TEXT,
    wegeart TEXT,
    strassenschluessel TEXT,
    europastrasse TEXT,
    geom geometry(LineString, 25832) NOT NULL,
    CONSTRAINT road_network_pkey PRIMARY KEY (feature_id)
);

-- Spatial index for geometry operations.
CREATE INDEX road_network_geom_gix
    ON public.road_network
    USING GIST (geom);
