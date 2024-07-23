# 数字转字符串

```sql
-- 输出 10.01
select to_char(10.010,'fm99990.099' ) from dual
```

- `9` 如果存在数字则显示数字, 不存在显示空格
- `0` 如果存在数字则显示数字, 不存在则显示 0
- `fm` 删除 `9` 生成的空格

## 前面补 0

```sql
-- 如果不加fm, 前面会多出一个空格
-- 001
SELECT to_char(1, 'fm000') FROM dual
-- 001.100
SELECT to_char(1.1, 'fm000.000') FROM dual
```
