# 存储过程

## 基本使用

MySQL 默认的语句结束符号为分号, 而存储过程中 SQL 一旦用了分号就认为该句结束了, 所以导致存储过程不完整, 执行的时候提示上面的语法错误。解决方法也简单, 用`delimiter //` 语句将 MySQL 的结束符设置为 `//`, 最后再用`delimiter ;` 把结束符号改回原来的分号。

1. 创建

```sql
drop procedure if exists hello;
delimiter //
create procedure hello()
begin
    select 'hello world';
end //
delimiter ;
```

2. 调用

```sql
call hello();
```

3. 删除

```sql
drop procedure if exists hello;
```

## 传参

3 种参数类型

- `in 参数名 类型`: 表示调用者向过程传入值(传入值可以是字面量或变量)
- `out 参数名 类型`: 表示过程向调用者传出值(可以返回多个值)(传出值只能是变量)
- `inout 参数名 类型`: 既表示调用者向过程传入值, 又表示过程向调用者传出值(值只能是变量)

```sql
drop procedure if exists hello;
delimiter //
create procedure hello(in user_name varchar(10))
begin
    select concat('hello ', user_name);
end //
delimiter ;

-- 传参
call hello('zhangsan');
drop procedure if exists hello;
```

## 变量

```sql
drop procedure if exists hello;
delimiter //
create procedure hello()
begin
    -- 定义变量
    declare user_name varchar(10);
    -- 变量赋值
    SET user_name = 'zhangsan';

    select concat('hello ', user_name);
end //
delimiter ;

call hello();
drop procedure if exists hello;
```
