SELECT
    target_frame.country AS country,
    count(DISTINCT target_frame.url) AS cnt
FROM
    TARGET_FRAME
WHERE_CLAUSE
GROUP BY
    target_frame.country
ORDER BY
    cnt DESC