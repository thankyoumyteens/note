# 创建索引

```sql
alter table 表名 add index 索引名(列名);
```

## 创建联合索引

```sql
alter table 表名 add index 索引名(列名1,列名2,...);
```

## 创建前缀索引

```sql
alter table 表名 add index 索引名(列名(前缀长度));
```
