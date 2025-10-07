# 变量

在 MySQL 中，变量分为用户变量、会话变量、全局变量和局部变量(存储过程/函数中)。

## 用户变量(User Variables)

用户变量是会话级别的变量，作用域为当前连接，无需提前声明，直接赋值即可使用，命名以 `@` 开头。

```sql
-- 使用SET语句赋值
SET @var1 = 100;
SET @var2 = 'hello';
SET @var3 = (SELECT COUNT(*) FROM employees); -- 子查询赋值

-- 使用SELECT语句赋值
SELECT @var4 := MAX(salary) FROM employees;
SELECT name, @var5 := age FROM users WHERE id = 1; -- 同时查询和赋值
```

## 会话变量(Session Variables)

会话变量作用域为当前会话，由 MySQL 预定义或用户设置，命名以 `@@session.` 开头(可省略 `session.`)。

```sql
-- 设置会话变量
SET @@session.auto_commit = 0; -- 关闭当前会话自动提交
SET auto_commit = 1; -- 省略session.，等价于上面的语句

-- 查看会话变量
SELECT @@session.auto_commit;
SELECT @@auto_commit;
```

## 全局变量(Global Variables)

全局变量作用域为所有会话(需 SUPER 权限)，命名以 `@@global.`开头(不可省略)。

```sql
-- 设置全局变量(影响新会话，当前会话需重新连接生效)
SET @@global.max_connections = 1000;

-- 查看全局变量
SELECT @@global.max_connections;
```

## 局部变量(Local Variables)

局部变量仅在存储过程、函数、触发器中使用，作用域为声明它的 `BEGIN...END `块，需用 `DECLARE` 声明，且必须在块的开头。

```sql
DELIMITER //
CREATE PROCEDURE get_employee_salary(IN emp_id INT)
BEGIN
  -- 声明局部变量
  DECLARE emp_name VARCHAR(50);
  -- 带默认值的局部变量
  DECLARE emp_salary DECIMAL(10,2) DEFAULT 0;

  -- 赋值方式1：SET
  SET emp_name = (SELECT name FROM employees WHERE id = emp_id);

  -- 赋值方式2：SELECT ... INTO
  SELECT salary INTO emp_salary FROM employees WHERE id = emp_id;

  -- 使用变量
  SELECT emp_name, emp_salary;
END //
DELIMITER ;

-- 调用存储过程
CALL get_employee_salary(1001);
```
