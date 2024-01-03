SELECT
    count(DISTINCT url) AS cnt
FROM
    output_frame
WHERE_CLAUSE