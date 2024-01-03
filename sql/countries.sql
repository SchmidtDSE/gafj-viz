SELECT
    country AS country,
    count(DISTINCT url) AS cnt
FROM
    output_frame
WHERE_CLAUSE
GROUP BY
    country
ORDER BY
    cnt DESC
LIMIT 10