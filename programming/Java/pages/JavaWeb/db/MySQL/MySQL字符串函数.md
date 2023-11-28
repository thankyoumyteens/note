# CONV()

进制转换, 返回数字的字符串表示。

当定义的参数为NULL时, 返回值将为NULL。

最小基数为2, 最大基数为36。如果要转换的基数为负数, 则该数字被视为带符号数。否则被当作无符号数

语法
```sql
CONV(NUM,from_base,to_base)
```
参数

- NUM: 被转换的数
- from_base: 从几进制
- to_base: 转换到几进制

示例
```sql
-- 把16进制数'a'转换成二进制
select CONV("a",16,2);
-- 输出: '1010'
```

# CONCAT()

返回来自于参数连结的字符串。如果任何参数是NULL, 返回NULL。可以有超过2个的参数。一个数字参数被变换为等价的字符串形式。

语法
```sql
CONCAT(str1,str2,...)
```

示例
```sql
select CONCAT('My', 'S', 'QL');
-- 输出: 'MySQL'
```

# GROUP_CONCAT()

把查询结果拼接成字符串

语法
```sql
GROUP_CONCAT([distinct] 要连接的字段 [order by 排序字段 asc/desc ] [separator '分隔符'] )
```

示例
```sql
select GROUP_CONCAT(concat('"',role_id,'"') separator ',') from role_info;
-- 输出: "123","456","789","111"
```

# CONCAT_WS()

CONCAT With Separator , 是CONCAT()的特殊形式。第一个参数是其它参数的分隔符。分隔符的位置放在要连接的两个字符串之间。分隔符可以是一个字符串, 也可以是其它参数。

语法
```sql
CONCAT_WS(separator,str1,str2,...)
```

示例
```sql
SELECT CONCAT_WS(";",'aa','bb');
-- 输出: 'aa;bb'
```

# LENGTH()

返回字符串的字节数

语法
```sql
LENGTH(str)
```

# CHAR_LENGTH()

返回字符串的字符数

语法
```sql
CHAR_LENGTH(str)
```

# LOCATE()

返回子串substr在字符串str第一个出现的位置(从1开始), 从位置pos开始。如果substr不是在str里面, 返回0。

语法
```sql
LOCATE(substr,str[,pos])
```

# LPAD()/RPAD()

返回字符串str, 左面用字符串padstr填补直到str是len个字符长。

语法
```sql
LPAD(str,len,padstr)
```

返回字符串str, 右面用字符串padstr填补直到str是len个字符长。

语法
```sql
RPAD(str,len,padstr)
```

# SUBSTRING()

从字符串str返回一个len个字符的子串, 从位置pos开始。

语法
```sql
SUBSTRING(str,pos[,len])
```

# TRIM()

过滤指定的字符串

语法
```sql
TRIM([{BOTH | LEADING | TRAILING} [remstr] FROM] str) 
```

示例
```sql
-- 默认删除前后空格 'bar'
SELECT TRIM(' bar ');
-- 删除句首逗号 'barxxx'
SELECT TRIM(LEADING ', ' FROM ', , barxxx');
-- 删除首尾逗号 'bar'
SELECT TRIM(BOTH ', ' FROM ', , bar, , , ');
-- 删除句尾逗号 'barxxyz'
SELECT TRIM(TRAILING ', ' FROM 'barxxyz, , ');
```

# REPLACE()

语法
```sql
REPLACE(str,from_str,to_str)
```

示例
```sql
select REPLACE('www.mysql.com', 'w', 'Ww');
-- 输出: 'WwWwWw.mysql.com'
```

# REVERSE()

反转字符串

语法
```sql
REVERSE(str)
```

# LOWER()/UPPER()

把所有的字符改变成大/小写

语法
```sql
UPPER(str)
LOWER(str)
```
