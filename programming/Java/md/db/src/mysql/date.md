# 日期操作

## 日期格式化

```sql
select date_format(now(),'%Y-%m-%d %H:%i:%s');
-- 格式化时间戳
SELECT FROM_UNIXTIME(UNIX_TIMESTAMP(),'%Y-%m-%d %H:%i:%s');
-- 格式化13位时间戳
SELECT FROM_UNIXTIME(1627311955999/1000,'%Y-%m-%d %H:%i:%s');
```

## 日期加减

```sql
--加1年
select date_add(now(),interval 1 year);
--加1月
select date_add(now(),interval 1 month);
--加1星期
select date_add(now(),interval 1 week);
--加1天
select date_add(now(),interval 1 day);
--加1小时
select date_add(now(),interval 1 hour);
--加1分钟
select date_add(now(),interval 1 minute);
--加1秒
select date_add(now(),interval 1 second);

--减1年
select date_sub(now(),interval 1 year);
--减1月
select date_sub(now(),interval 1 month);
--减1星期
select date_sub(now(),interval 1 week);
--减1天
select date_sub(now(),interval 1 day);
--减1小时
select date_sub(now(),interval 1 hour);
--减1分钟
select date_sub(now(),interval 1 minute);
--减1秒
select date_sub(now(),interval 1 second);
```
