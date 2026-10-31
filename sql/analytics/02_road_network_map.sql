CREATE OR REPLACE VIEW analytics.v_road_network_map AS
SELECT
    feature_id,
    strassenname,
    klasse,
    wegeart,
    wegenummer,
    geschwindigkeit,
    abschnittslaenge,
    fahrstreifenanzahl_in_stationierungsrichtung,
    fahrstreifenanzahl_in_beide_richtungen,
    fahrstreifenanzahl_gegen_stationierungsrichtung,
    bahnigkeit,
    geom
FROM public.road_network;
