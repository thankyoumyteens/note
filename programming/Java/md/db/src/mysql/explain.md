# explain

直接在 sql 语句前加上 explain 或 desc 就可以获取 sql 执行的信息。

```sql
explain select * from name_info;
```

输出:

```
| id   | select_type | table     | type | possible_keys | key  | key_len | ref  | rows | Extra |
+------+-------------+-----------+------+---------------+------+---------+------+------+-------+
|    1 | SIMPLE      | name_info | ALL  | NULL          | NULL | NULL    | NULL |    1 |       |
+------+-------------+-----------+------+---------------+------+---------+------+------+-------+
1 row in set (0.00 sec)
```
