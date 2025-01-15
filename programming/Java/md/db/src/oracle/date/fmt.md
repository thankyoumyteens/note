# 日期格式化

```sql
select to_char(sysdate, 'yyyy-mm-dd hh24:mi:ss') from dual;
-- date类型只能精确到秒, 要想精确到毫秒, 需要使用timestamp类型
-- ff1: 表示1位毫秒, 范围是0-9
-- ff2: 表示2位毫秒, 范围是00-99
-- ff3: 表示3位毫秒, 范围是000-999
-- ff4: 表示4位毫秒, 范围是0000-9999
select to_char(systimestamp, 'yyyy-mm-dd hh24:mi:ss.ff3') from dual;
```
