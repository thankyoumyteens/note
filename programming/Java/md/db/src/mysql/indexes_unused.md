# 索引失效

## 使用联合索引时, 违反了最左匹配原则

创建测试表(MySQL5.7)

```sql
CREATE TABLE `test_user` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT PRIMARY KEY COMMENT '主键',
  `username` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '用户名',
  `email` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '用户邮箱',
  `status` tinyint(1) DEFAULT '0' NOT NULL COMMENT '用户状态',
  `bio` text COLLATE utf8mb4_unicode_ci COMMENT '个人简介'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

创建联合索引

```sql
create index `test_user_index_1` on `test_user`(`username`, `email`, `status`);
```

### 走索引的情况

```sql
-- 遵循 `username`, `email`, `status` 从左到右的顺序
explain select * from `test_user` where `username` = 'ccc';
```

结果:

| id  | select_type | table     | partitions | type | possible_keys     | key               | key_len | ref   | rows | filtered | Extra |
| --- | ----------- | --------- | ---------- | ---- | ----------------- | ----------------- | ------- | ----- | ---- | -------- | ----- |
| 1   | SIMPLE      | test_user |            | ref  | test_user_index_1 | test_user_index_1 | 202     | const | 1    | 100.0    |       |

```sql
-- 遵循 `username`, `email`, `status` 从左到右的顺序
explain select * from `test_user` where `username` = 'ccc' and `email` = 'ccc@123.com';
-- 和上面的一样, 虽然没有按从左到右的顺序写, 但mysql会把它优化成上面那样
explain select * from `test_user` where `email` = 'ccc@123.com' and `username` = 'ccc';
```

结果:

| id  | select_type | table     | partitions | type | possible_keys     | key               | key_len | ref         | rows | filtered | Extra |
| --- | ----------- | --------- | ---------- | ---- | ----------------- | ----------------- | ------- | ----------- | ---- | -------- | ----- |
| 1   | SIMPLE      | test_user |            | ref  | test_user_index_1 | test_user_index_1 | 604     | const,const | 1    | 100.0    |       |

```sql
-- 遵循 `username`, `email`, `status` 从左到右的顺序
explain select * from `test_user` where `username` = 'ccc' and `email` = 'ccc@123.com' and `status` = 1;
-- 和上面的一样, 虽然没有按从左到右的顺序写, 但mysql会把它优化成上面那样
explain select * from `test_user` where `status` = 1 and `email` = 'ccc@123.com' and `username` = 'ccc';
-- 同理
explain select * from `test_user` where `email` = 'ccc@123.com' and `status` = 1 and `username` = 'ccc';
explain select * from `test_user` where `username` = 'ccc' and `status` = 1 and `email` = 'ccc@123.com';
```

结果:

| id  | select_type | table     | partitions | type | possible_keys     | key               | key_len | ref               | rows | filtered | Extra |
| --- | ----------- | --------- | ---------- | ---- | ----------------- | ----------------- | ------- | ----------------- | ---- | -------- | ----- |
| 1   | SIMPLE      | test_user |            | ref  | test_user_index_1 | test_user_index_1 | 605     | const,const,const | 1    | 100.0    |       |

其中, 随着使用的联合索引中的字段越来越多, key_len 也不断增长。

### 索引失效的情况

```sql
-- 缺少最左的字段 `username`, 索引失效
explain select * from `test_user` where `email` = 'ccc@123.com';
explain select * from `test_user` where `status` = 1;
explain select * from `test_user` where `email` = 'ccc@123.com' and `status` = 1;
```

| id  | select_type | table     | partitions | type | possible_keys | key | key_len | ref | rows | filtered | Extra       |
| --- | ----------- | --------- | ---------- | ---- | ------------- | --- | ------- | --- | ---- | -------- | ----------- |
| 1   | SIMPLE      | test_user |            | ALL  |               |     |         |     | 3    | 33.33    | Using where |

```sql
-- 有最左的字段 `username`, 缺少中间的 `email`, 所以只有 `username` 生效了
explain select * from `test_user` where `status` = 1 and `username` = 'ccc';
explain select * from `test_user` where `username` = 'ccc' and `status` = 1;
```

| id  | select_type | table     | partitions | type | possible_keys     | key               | key_len | ref   | rows | filtered | Extra                 |
| --- | ----------- | --------- | ---------- | ---- | ----------------- | ----------------- | ------- | ----- | ---- | -------- | --------------------- |
| 1   | SIMPLE      | test_user |            | ref  | test_user_index_1 | test_user_index_1 | 202     | const | 1    | 33.33    | Using index condition |

key_len 和查询条件只有 `username` 时的值一致。

## 在索引列上进行运算时, 索引失效

```sql
explain select * from `test_user` where substring(`username`, 1, 2) = 'cc';
```

| id  | select_type | table     | partitions | type | possible_keys | key | key_len | ref | rows | filtered | Extra       |
| --- | ----------- | --------- | ---------- | ---- | ------------- | --- | ------- | --- | ---- | -------- | ----------- |
| 1   | SIMPLE      | test_user |            | ALL  |               |     |         |     | 3    | 100.0    | Using where |

## 以%开头的 like 查询, 索引失效

```sql
-- 索引生效
explain select * from `test_user` where `username` like 'c%';
```

| id  | select_type | table     | partitions | type  | possible_keys     | key               | key_len | ref | rows | filtered | Extra                 |
| --- | ----------- | --------- | ---------- | ----- | ----------------- | ----------------- | ------- | --- | ---- | -------- | --------------------- |
| 1   | SIMPLE      | test_user |            | range | test_user_index_1 | test_user_index_1 | 202     |     | 1    | 100.0    | Using index condition |

```sql
-- 索引失效
explain select * from `test_user` where `username` like '%c';
explain select * from `test_user` where `username` like '%c%';
```

| id  | select_type | table     | partitions | type | possible_keys | key | key_len | ref | rows | filtered | Extra       |
| --- | ----------- | --------- | ---------- | ---- | ------------- | --- | ------- | --- | ---- | -------- | ----------- |
| 1   | SIMPLE      | test_user |            | ALL  |               |     |         |     | 3    | 33.33    | Using where |
