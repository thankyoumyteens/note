# 生成指定时间范围内的每一天日期

生成 2025-01-01 到 2025-02-11 (包含) 期间每一天的日期

```sql
-- 利用系统表生成数字序列（无需手动创建数字表）
SELECT
    DATE_ADD('2025-01-01', INTERVAL t.n DAY) AS date
FROM
    (
        SELECT
            @row := @row + 1 AS n
        FROM
            information_schema.columns c1,
            information_schema.columns c2,
            (SELECT @row := -1) r
        LIMIT 42  -- 总天数：从2025-01-01到2025-02-11共42天
    ) t
WHERE
    DATE_ADD('2025-01-01', INTERVAL t.n DAY) <= '2025-02-11';

```

## mysql8.0 及以上版本

```sql
WITH RECURSIVE date_series AS (
    SELECT '2025-01-01' AS date  -- 起始日期
    UNION ALL
    SELECT DATE_ADD(date, INTERVAL 1 DAY)
    FROM date_series
    WHERE date < '2025-02-11'  -- 结束日期
)
SELECT date FROM date_series;
```
