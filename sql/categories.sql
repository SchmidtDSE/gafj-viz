SELECT
    output_frame.token AS token,
    count(DISTINCT output_frame.url) AS cnt
FROM
    output_frame
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
    output_frame.url = match_url.url
WHERE
    output_frame.tokenType = 'category'
GROUP BY
    output_frame.token
ORDER BY
    cnt DESC
LIMIT 10