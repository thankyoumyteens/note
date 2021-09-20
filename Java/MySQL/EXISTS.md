# SQL中的EXISTS

可以理解为：将外查询表的每一行，代入内查询作为检验，如果内查询返回的结果取非空值，则EXISTS子句返回TRUE，这一行行可作为外查询的结果行，否则不能作为结果。

```sql
SELECT *
    FROM class AS c1
    WHERE EXISTS(SELECT
               class_id
             FROM class AS c2
             WHERE c1.class_id = 5);
```

- 如果exists里面返回的结果行数大于1，则返回true，则外面的查询数据可以返回。
- 如果exsits返回的是false，则外层查询无效，也就不会返回数据。
