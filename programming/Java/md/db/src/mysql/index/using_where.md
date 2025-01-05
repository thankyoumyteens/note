# Using where

使用了非等值查询, 且没有索引参加。

```sql
-- student_phone不是索引
desc select * from student_info where student_phone >= '13512345670';
```

使用了非等值查询, 有索引参加。

```sql
-- student_age是索引
desc select * from student_info where student_age >= 10;
```
