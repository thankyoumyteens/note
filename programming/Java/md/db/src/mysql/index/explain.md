# 执行计划

直接在 sql 语句前加上 explain 或 desc 就可以获取 sql 执行的信息。

```sql
desc select * from name_info;
```

输出:

```
| id   | select_type | table     | type | possible_keys | key  | key_len | ref  | rows | Extra |
+------+-------------+-----------+------+---------------+------+---------+------+------+-------+
|    1 | SIMPLE      | name_info | ALL  | NULL          | NULL | NULL    | NULL |    1 |       |
+------+-------------+-----------+------+---------------+------+---------+------+------+-------+
1 row in set (0.00 sec)
```

- id: 表示执行顺序, id 大的先执行, id 相同的从上到下执行
- type: sql 的连接类型, 性能由好到差分别是 NULL, system, const, eq_ref, ref, range, index, all
  - system: 查询 mysql 的系统表
  - const: 根据主键等值查询(`=`)
  - eq_ref: 主键索引或唯一索引等值查询(`=`)
  - ref: 二级索引等值查询(`=`)
  - range: 使用索引, 但 sql 是范围查询(`> < >= <= between in or`)
  - index: 遍历整个索引树查询
  - all: 全表扫描
- possible_keys: 当前 sql 可能使用到的索引
- key: 当前 sql 实际用到的索引
- key_len: 索引占用的大小(可以通过计算判断用到了联合索引中的哪几个索引)
- rows: 本次查询预估要扫描多少行
- Extra: 额外的优化建议
  - Using where; Using Index: 查找使用了索引, 需要的数据都在索引中能找到, 不需要回表查询数据
  - Using index condition: 查找使用了索引, 但是需要回表查询数据

## 指定输出格式

- `desc format=json select ...` 以 json 格式输出
- `desc format=tree select ...` 以树形结构输出
