# 小数点前 0 不显示

比如 0.3 会显示成 .3。

解决:

```sql
-- 保留两位小数
select to_char(DATA_RATE, 'fm9990.09') from dual;
```
