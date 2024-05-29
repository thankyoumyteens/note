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
