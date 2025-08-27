# 生成 12 个月月份

```sql
SELECT DATE_FORMAT(STR_TO_DATE(CONCAT('2025', LPAD(n, 2, '0'), '01'), '%Y%m%d'), '%Y-%m') AS month
FROM (
    SELECT 1 AS n UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL
    SELECT 4 UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL
    SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9 UNION ALL
    SELECT 10 UNION ALL SELECT 11 UNION ALL SELECT 12
) AS numbers;
```

## mysql8.0 及以上版本

```sql
WITH RECURSIVE year_months AS (
    SELECT '2025-01' AS month  -- 起始月份
    UNION ALL
    SELECT DATE_FORMAT(
        DATE_ADD(STR_TO_DATE(CONCAT(month, '-01'), '%Y-%m-%d'), INTERVAL 1 MONTH),
        '%Y-%m'
    ) AS month
    FROM year_months
    WHERE month < '2025-12'  -- 结束月份
)
SELECT month FROM year_months;
```
