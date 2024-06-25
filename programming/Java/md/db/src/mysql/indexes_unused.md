# 索引失效

## 使用联合索引时, 违反了最左匹配原则

创建测试表

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
