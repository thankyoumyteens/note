# 日期加减

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
