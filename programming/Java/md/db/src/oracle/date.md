# 日期操作

## 日期格式化

```sql
select to_char(sysdate, 'yyyy-mm-dd hh24:mi:ss') from dual;
-- date类型只能精确到秒, 要想精确到毫秒, 需要使用timestamp类型
-- ff1: 表示1位毫秒, 范围是0-9
-- ff2: 表示2位毫秒, 范围是00-99
-- ff3: 表示3位毫秒, 范围是000-999
-- ff4: 表示4位毫秒, 范围是0000-9999
select to_char(systimestamp, 'yyyy-mm-dd hh24:mi:ss.ff3') from dual;
```

## 日期加减

```sql
--加1年
select add_months(sysdate,12) from dual;
--加1月
select add_months(sysdate,1) from dual;
--加1星期
select to_char(sysdate+7,'yyyy-mm-dd HH24:MI:SS') from dual;
--加1天
select to_char(sysdate+1,'yyyy-mm-dd HH24:MI:SS') from dual;
--加1小时
select to_char(sysdate+1/24,'yyyy-mm-dd HH24:MI:SS') from dual;
--加1分钟
select to_char(sysdate+1/24/60,'yyyy-mm-dd HH24:MI:SS') from dual;
--加1秒
select to_char(sysdate+1/24/60/60,'yyyy-mm-dd HH24:MI:SS') from dual;

--减1年
select add_months(sysdate,-12) from dual;
--减1月
select add_months(sysdate,-1) from dual;
--减1星期
select to_char(sysdate-7,'yyyy-mm-dd HH24:MI:SS') from dual;
--减1天
select to_char(sysdate-1,'yyyy-mm-dd HH24:MI:SS') from dual;
--减1小时
select to_char(sysdate-1/24,'yyyy-mm-dd HH24:MI:SS') from dual;
--减1分钟
select to_char(sysdate-1/24/60,'yyyy-mm-dd HH24:MI:SS') from dual;
--减1秒
select to_char(sysdate-1/24/60/60,'yyyy-mm-dd HH24:MI:SS') from dual;
```

## 日期截取

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
