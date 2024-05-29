# 生成指定时间范围内的每一天日期

```sql
select
    to_date(#{startTime}, 'yyyy-MM-dd') + rownum - 1 as dateday
from
    dual
connect by
    rownum <= (
        to_date(#{endTime}, 'yyyy-MM-dd') - to_date(#{startTime}, 'yyyy-MM-dd') + 1
    );
```
