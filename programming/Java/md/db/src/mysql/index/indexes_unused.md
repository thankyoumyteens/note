# 索引失效的情况

## 以%开头的 like 查询, 索引失效

```sql
-- 索引生效
explain select * from `test_user` where `username` like 'c%';

-- 索引失效
explain select * from `test_user` where `username` like '%c';
explain select * from `test_user` where `username` like '%c%';
```

## 使用联合索引时, 违反了最左匹配原则

联合索引

```sql
(`username`, `email`, `status`)
```

```sql
-- 索引生效
-- 遵循 `username`, `email`, `status` 从左到右的顺序
explain select * from `test_user` where `username` = 'ccc';
-- 遵循 `username`, `email`, `status` 从左到右的顺序
explain select * from `test_user` where `username` = 'ccc' and `email` = 'ccc@123.com';
-- 和上面的一样, 虽然没有按从左到右的顺序写, 但mysql会把它优化成上面那样
explain select * from `test_user` where `email` = 'ccc@123.com' and `username` = 'ccc';
-- 遵循 `username`, `email`, `status` 从左到右的顺序
explain select * from `test_user` where `username` = 'ccc' and `email` = 'ccc@123.com' and `status` = 1;
-- 和上面的一样, 虽然没有按从左到右的顺序写, 但mysql会把它优化成上面那样
explain select * from `test_user` where `status` = 1 and `email` = 'ccc@123.com' and `username` = 'ccc';
-- 同理
explain select * from `test_user` where `email` = 'ccc@123.com' and `status` = 1 and `username` = 'ccc';
explain select * from `test_user` where `username` = 'ccc' and `status` = 1 and `email` = 'ccc@123.com';

-- 索引失效
-- 缺少最左的字段 `username`, 索引失效
explain select * from `test_user` where `email` = 'ccc@123.com';
explain select * from `test_user` where `status` = 1;
explain select * from `test_user` where `email` = 'ccc@123.com' and `status` = 1;
-- 有最左的字段 `username`, 缺少中间的 `email`, 所以只有 `username` 生效了
explain select * from `test_user` where `status` = 1 and `username` = 'ccc';
explain select * from `test_user` where `username` = 'ccc' and `status` = 1;
```

## 在索引列上进行运算时, 索引失效

```sql
explain select * from `test_user` where substring(`username`, 1, 2) = 'cc';
```
