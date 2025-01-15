# 生成随机日期

```sql
-- 生成2020-01-01 00:00:00至2020-12-31 23:59:59内的日期时间
SELECT to_date(TRUNC(DBMS_RANDOM.VALUE(
       to_number(to_char(to_date('20200101','yyyymmdd'),'J')),
       to_number(to_char(to_date('20201231','yyyymmdd')+1,'J')))),'J')+
       DBMS_RANDOM.VALUE(1,3600)/3600
       prize_time
FROM dual;
```
