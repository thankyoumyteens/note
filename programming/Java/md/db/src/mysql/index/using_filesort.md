# Using filesort

在使用 order by 关键字的时候, 如果待排序的内容不能由所使用的索引直接完成排序的话, 那么 mysql 有可能就要进行文件排序。这个 filesort 并不是说通过磁盘文件进行排序, 而只是告诉我们进行了一个排序操作而已。

比如:

```sql
-- 给create_time建立索引也没用
desc select student_id, student_age from student_info where student_age = 10 order by create_time desc;
```

解决方法: 为 where 和 order by 用到的列建立联合索引:

```sql
alter table student_info add index idx_age_time(student_age, create_time);
```
