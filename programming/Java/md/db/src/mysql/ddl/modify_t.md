# 修改表

```sql
-- 修改表名
rename table 表名 to 新的表名;

-- 修改存储引擎
alter table 表名 engine=引擎名;

-- 修改字符集
alter table 表名 charset=字符集;

-- 修改注释
alter table 表名 comment=注释;
```

## 列操作

```sql
-- 增加列
alter table student_info add update_time datetime not null default now() comment '修改时间';

-- 修改列
alter table student_info modify update_time varchar(20) not null default '' comment '修改时间';

-- 删除列
alter table student_info drop update_time;
```

## 索引操作

```sql
-- 添加索引
alter table student_info add index 索引名(列名);
```
