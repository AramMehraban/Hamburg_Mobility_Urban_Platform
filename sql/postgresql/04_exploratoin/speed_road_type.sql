SELECT
    klasse,
    COUNT(*) AS segment_count,
    COUNT(DISTINCT wegeart) AS different_road_types,
    COUNT(DISTINCT geschwindigkeit) AS different_speed_values
FROM public.road_network
GROUP BY klasse
ORDER BY klasse;


-- Analyze Missing Speed Values and Road Types
SELECT
    klasse,
    COUNT(*) AS total_segments,

    COUNT(*) FILTER (
        WHERE NULLIF(BTRIM(wegeart::text), '') IS NULL
    ) AS missing_road_type,

    COUNT(*) FILTER (
        WHERE NULLIF(BTRIM(geschwindigkeit::text), '') IS NULL
    ) AS missing_speed,

    COUNT(DISTINCT wegeart) AS distinct_road_types,
    COUNT(DISTINCT geschwindigkeit) AS distinct_speeds

FROM public.road_network
GROUP BY klasse
ORDER BY klasse;


-- Count Speed Values by Road Class
SELECT
    klasse,
    geschwindigkeit,
    COUNT(*) AS segment_count
FROM public.road_network
GROUP BY
    klasse,
    geschwindigkeit
ORDER BY
    klasse,
    segment_count DESC;


-- Classify Speed Limit Values
WITH speed_profile AS (
    SELECT
        klasse,
        geschwindigkeit,
        CASE
            WHEN NULLIF(BTRIM(geschwindigkeit::text), '') IS NULL
                THEN '01 - Fehlender Wert'

            WHEN geschwindigkeit::text ILIKE '%Nicht mit KFZ befahrbar%'
                THEN '02 - Nicht mit Kfz befahrbar'

            WHEN geschwindigkeit::text ILIKE '%Verkehrsbeeinflussungsanlage%'
                THEN '03 - Variable Geschwindigkeitsregelung'

            WHEN geschwindigkeit::text ILIKE '%ohne Geschwindigkeitsbegrenzung%'
                THEN '04 - Ohne Geschwindigkeitsbegrenzung'

            WHEN geschwindigkeit::text LIKE '%|%'
                THEN '05 - Mehrere Angaben kombiniert'

            WHEN geschwindigkeit::text ~* '[0-9]+-[0-9]+ *km/h'
                THEN '06 - Geschwindigkeitsbereich'

            WHEN geschwindigkeit::text ~* '[0-9]+ *km/h'
                AND geschwindigkeit::text LIKE '%(%'
                THEN '07 - Zeit- oder Sonderregelung'

            WHEN geschwindigkeit::text ~* '[0-9]+ *km/h'
                THEN '08 - Geschwindigkeitsangabe'

            ELSE '09 - Sonstige Angabe'
        END AS speed_category
    FROM public.road_network
)
SELECT
    klasse,
    speed_category,
    COUNT(*) AS segment_count
FROM speed_profile
GROUP BY klasse, speed_category
ORDER BY klasse, speed_category;


-- Identify Unclassified Speed Values
SELECT
    klasse,
    geschwindigkeit,
    COUNT(*) AS segment_count
FROM public.road_network
WHERE
    NULLIF(BTRIM(geschwindigkeit::text), '') IS NOT NULL
    AND geschwindigkeit::text NOT ILIKE '%Nicht mit KFZ befahrbar%'
    AND geschwindigkeit::text NOT ILIKE '%Verkehrsbeeinflussungsanlage%'
    AND geschwindigkeit::text NOT ILIKE '%ohne Geschwindigkeitsbegrenzung%'
    AND geschwindigkeit::text NOT LIKE '%|%'
    AND geschwindigkeit::text !~* '[0-9]+-[0-9]+ *km/h'
    AND geschwindigkeit::text !~* '[0-9]+ *km/h'
GROUP BY klasse, geschwindigkeit
ORDER BY klasse, segment_count DESC;


-- Classify Speed Values by Road Class
WITH speed_profile AS (
    SELECT
        klasse,
        geschwindigkeit,
        CASE
            WHEN NULLIF(BTRIM(geschwindigkeit::text), '') IS NULL
                THEN '01 - Fehlender Wert'

            WHEN geschwindigkeit::text ILIKE '%Nicht mit KFZ befahrbar%'
                THEN '02 - Nicht mit Kfz befahrbar'

            WHEN geschwindigkeit::text ILIKE '%Verkehrsbeeinflussungsanlage%'
                THEN '03 - Variable Geschwindigkeitsregelung'

            WHEN geschwindigkeit::text ILIKE '%ohne Geschwindigkeitsbegrenzung%'
                THEN '04 - Ohne Geschwindigkeitsbegrenzung'

            WHEN geschwindigkeit::text ILIKE '%Autobahn-Auffahrt%'
                THEN '05 - Autobahnauffahrt ohne explizite Begrenzung'

            WHEN geschwindigkeit::text LIKE '%|%'
                THEN '06 - Mehrere Angaben kombiniert'

            WHEN geschwindigkeit::text ~* '[0-9]+-[0-9]+ *km/h'
                THEN '07 - Geschwindigkeitsbereich'

            WHEN geschwindigkeit::text ~* '[0-9]+ *km/h'
                 AND geschwindigkeit::text LIKE '%(%'
                THEN '08 - Zeit- oder Sonderregelung'

            WHEN geschwindigkeit::text ~* '[0-9]+ *km/h'
                THEN '09 - Geschwindigkeitsangabe'

            ELSE '10 - Sonstige Angabe'
        END AS speed_category
    FROM public.road_network
)
SELECT
    klasse,
    speed_category,
    COUNT(*) AS segment_count
FROM speed_profile
GROUP BY klasse, speed_category
ORDER BY klasse, speed_category;


-- Calculate Missing Speed Values by Road Class
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

FROM public.road_network
GROUP BY klasse
ORDER BY klasse;