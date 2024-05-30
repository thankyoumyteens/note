# oracle 排序后, 分页数据重复 / oracle 排序后, 切换页大小数据乱序

Oracle 的排序算法不具有稳定性, 对于排序键值相等的数据, 这种算法完成排序后, 不能保证这些键值相等的数据保持排序前的顺序。

比如:

```sql
select *
from MY_TABLE
order by CREATE_TIME desc
```

如果 CREATE_TIME 相同, 那排序后的数据是不确定的。如果 CREATE_TIME 相等的两条正好处在第一页末尾和第二页开头, 那在查第二页时, 第一页末尾的数据会覆盖第二页开头的数据。

如果切换每页显示的条数, 10 页/条 和 20 页/条展示的数据顺序也可能会不同。

## 解决

在 order by 最后, 增加具有唯一索引的列或 ROWNUM:

```sql
select *
from MY_TABLE
order by CREATE_TIME desc, ROWNUM desc
```

或者:

```sql
select *
from MY_TABLE
order by CREATE_TIME desc, ID desc
```
