# 生成 12 个月月份

```sql
select
    lpad(level, 2, 0) || '月' as PER_MONTH
from
    DUAL
connect by
    level < 13;
```
