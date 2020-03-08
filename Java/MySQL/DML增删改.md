# DML：增删改表中数据

添加数据
```sql
insert into 表名(
  列名1,
  列名2,
  ...,
  列名n
) values(
  值1,
  值2,
  ...,
  值n
);
```
删除数据
```sql
delete from 表名 [where 条件];
```
删除所有记录
```sql
-- 先删除表,再创建一张一样的表
truncate table 表名;
```
修改数据
```sql
update 表名 
set 列名1=值1,列名2=值2,... 
[where 条件];
```
