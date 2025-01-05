# Using index

使用索引索引等值查询, 并且 sql 所需要返回的所有列均在一棵索引树上, 而无需回表。这类 SQL 语句往往性能较好。

```sql
-- student_age是索引
desc select student_age from student_info where student_age = 10;
```
