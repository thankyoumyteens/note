# 日期截取

```sql
 -- 2024-05-31 13:40:56.000
select sysdate from dual;
 -- 当天的日期 2024-05-31 00:00:00.000
select trunc(sysdate), sysdate from dual;
 -- 返回当月第一天 2024-05-01 00:00:00.000
select trunc(sysdate, 'mm'), sysdate from dual;
-- 返回当年第一天 2024-01-01 00:00:00.000
select trunc(sysdate,'yy'), sysdate from dual;
-- 返回当年第一天 2024-01-01 00:00:00.000
select trunc(sysdate,'yyyy'), sysdate from dual;
 -- 返回当前年月日 2024-05-31 00:00:00.000
select trunc(sysdate,'dd'), sysdate from dual;
-- 返回当前星期的第一天(星期天) 2024-05-26 00:00:00.000
select trunc(sysdate,'d'), sysdate from dual;
--返回当前时间小时取整 2024-05-31 13:00:00.000
select trunc(sysdate, 'hh'), sysdate from dual;
--返回当前时间分钟取整 2024-05-31 13:40:00.000
select trunc(sysdate, 'mi'), sysdate from dual;
```
