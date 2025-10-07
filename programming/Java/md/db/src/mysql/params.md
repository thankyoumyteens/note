# 传参

有 3 种参数类型:

- `in 参数名 类型`: 表示调用者向过程传入值(传入值可以是字面量或变量)
- `out 参数名 类型`: 表示过程向调用者传出值(可以返回多个值)(传出值只能是变量)
- `inout 参数名 类型`: 既表示调用者向过程传入值, 又表示过程向调用者传出值(值只能是变量)

```sql
delimiter //
-- 定义参数
create procedure hello(in user_name varchar(10))
begin
    select concat('hello ', user_name);
end //
delimiter ;

-- 传参
call hello('zhangsan');
```
