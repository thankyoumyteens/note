# SELECT INTO 和 INSERT INTO SELECT 两种表复制语句

## INSERT INTO SELECT语句

语句形式为：`Insert into Table2(field1,field2,...) select value1,value2,... from Table1`

要求目标表Table2必须存在, 由于目标表Table2已经存在, 所以我们除了插入源表Table1的字段外, 还可以插入常量。

示例如下:
```sql
Insert into Table2(a, c, d) select a,c,5 from Table1
```

## SELECT INTO FROM语句

语句形式为：`SELECT vale1, value2 into Table2 from Table1`

要求目标表Table2不存在, 因为在插入时会自动创建表Table2, 并将Table1中指定字段数据复制到Table2中。

示例如下:
```sql
select a,c INTO Table2 from Table1
```
