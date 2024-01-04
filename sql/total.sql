SELECT
    count(DISTINCT target_frame.url) AS cnt
FROM
    TARGET_FRAME
WHERE_CLAUSE