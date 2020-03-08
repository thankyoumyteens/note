# 数据表

创建表
```sql
create table 表名(
    列名1 数据类型1,
    列名2 数据类型2,
    ....
    列名n 数据类型n
);
```
复制表
```sql
create table 表名 like 被复制的表名;
```
查询数据库中所有的表
```sql
show tables;
```
查询表结构
```sql
desc 表名;
```
修改表名
```sql
alter table 表名 rename to 新的表名;
```
修改表的字符集
```sql
alter table 表名 character set 字符集名称;
```
添加列
```sql
alter table 表名 add 列名 数据类型;
```
删除列
```sql
alter table 表名 drop 列名;
```
修改列
```sql
alter table 表名 change 列名 新列名 新数据类型;
alter table 表名 modify 列名 新数据类型;
```
删除表
```sql
* drop table  if exists 表名 ;
```
