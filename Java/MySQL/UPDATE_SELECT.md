# MySQL update使用select的结果

## MySQL UPDATE JOIN语法

在MySQL中，可以在 UPDATE语句 中使用JOIN子句执行跨表更新。MySQL UPDATE JOIN的语法如下：
```sql
UPDATE T1
[INNER JOIN | LEFT JOIN] T2 ON T1.C1 = T2.C1
SET T1.C2 = T2.C2, 
    T2.C3 = expr
WHERE condition
```

更详细地看看MySQL UPDATE JOIN语法：
- 首先，在UPDATE子句之后，指定主表(T1)和希望主表连接表(T2)。
- 第二，指定一种要使用的连接，即INNER JOIN或LEFT JOIN和连接条件。JOIN子句必须出现在UPDATE子句之后。
- 第三，要为要更新的T1和/或T2表中的列分配新值。
- 第四，WHERE子句中的条件用于指定要更新的行。
