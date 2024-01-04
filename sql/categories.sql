SELECT
    target_frame.token AS token,
    count(DISTINCT target_frame.url) AS cnt
FROM
    TARGET_FRAME
INNER JOIN
    (
        SELECT
            url
        FROM
            output_frame
        WHERE_CLAUSE
            AND tokenType = 'category'
        GROUP BY
            url
    ) match_url
ON
    target_frame.url = match_url.url
WHERE
    target_frame.tokenType = 'category'
GROUP BY
    target_frame.token
ORDER BY
    cnt DESC
LIMIT 10