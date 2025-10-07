# 基本使用

MySQL 默认的语句结束符号为分号, 而存储过程中 SQL 一旦用了分号就认为该句结束了, 所以导致存储过程不完整, 执行的时候提示上面的语法错误。解决方法也简单, 用`delimiter //` 语句将 MySQL 的结束符设置为 `//`, 最后再用`delimiter ;` 把结束符号改回原来的分号。

### 1. 创建

```sql
drop procedure if exists hello;
delimiter //
create procedure hello()
begin
    select 'hello world';
end //
delimiter ;
```

### 2. 调用

```sql
call hello();
```

### 3. 删除

```sql
drop procedure if exists hello;
```
