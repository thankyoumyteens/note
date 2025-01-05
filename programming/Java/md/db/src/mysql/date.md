# 日期操作

DATETIME 和 TIMESTAMP 的区别:

- DATETIME 占用 8 个字节。存储的是固定的日期和时间值, 不受时区影响。范围从 1000-01-01 00:00:00 到 9999-12-31 23:59:59
- TIMESTAMP 占用 4 个字节。存储的是 Unix 时间戳(从 1970-01-01 00:00:00 UTC 开始的秒数), 并根据时区进行转换。范围从 1970-01-01 00:00:01 UTC 到 2038-01-19 03:14:07 UTC

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

## 日期间隔

```sql
-- 间隔几天
select TIMESTAMPDIFF(day, date1, date2);
select to_days('2020-01-02') - to_days('2020-01-01');
-- 间隔几月
select TIMESTAMPDIFF(month, date1, date2);
-- 间隔几年
select TIMESTAMPDIFF(year, date1, date2);
```

## 生成随机日期

```sql
-- 生成2020-01-01 00:00:00至2020-12-31 23:59:59内的日期时间
SELECT
    FROM_UNIXTIME(
        UNIX_TIMESTAMP('2020-01-01 00:00:00') +
        RAND() *
        (UNIX_TIMESTAMP('2020-12-31 23:59:59') - UNIX_TIMESTAMP('2020-01-01 00:00:00'))
    ) AS random_datetime;
```
