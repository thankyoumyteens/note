# CASE WHEN的两种写法

Type 1
```
CASE 列 WHEN [值] THEN 结果 [WHEN [值] THEN 结果 ...] [ELSE 结果] END
```

Type 2
```
CASE WHEN [条件] THEN 结果 [WHEN [条件] THEN 结果 ...] [ELSE 结果] END
```

# update 使用case when

```sql
UPDATE `goods` SET `type` = (
    CASE `name` WHEN 1 THEN 999  
    WHEN 2 THEN 1000  
    WHEN 3 THEN 1024  
    END)
WHERE ID in(1, 2, 3);
```

# select 使用case when

```sql
select *, (CASE WHEN age>=60 THEN ‘老年’ WHEN age<60 AND age>=30 THEN ‘中年’ WHEN age<30 AND age>=18 THEN ‘青年’ ELSE ‘未成年’ END) as age_text
from user
```

# sql 按指定规则排序, 例如 按 1,3,2排序 而不是1,2,3

```sql
SELECT TOP 3 id,Name FROM dbo.Company order by (case Id when 2 then 0 else Id end) ASC 
--或者
SELECT TOP 3 id,Name FROM dbo.Company order by (case Id when 2 then 0 else 1 end),Id asc
```
 