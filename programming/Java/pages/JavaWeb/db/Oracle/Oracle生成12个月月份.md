# Oracle生成12个月月份

```sql
select
    LPAD(level, 2, 0) || '月' as MONTH
from
    DUAL
connect by
    level < 13
```
