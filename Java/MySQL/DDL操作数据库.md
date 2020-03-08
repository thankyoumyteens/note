# 数据库
创建数据库：
```sql
create database if not exists 数据库名称 character set 字符集名;
```
查询所有数据库
```sql
show databases;
```
查询某个数据库的字符集
```sql
show create database 数据库名称;
```
修改数据库的字符集
```sql
alter database 数据库名称 character set 字符集名称;
```
删除数据库
```sql
drop database if exists 数据库名称;
```
却换到指定数据库
```sql
use 数据库名称;
```
