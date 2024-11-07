# 创建表

```sql
create table student_info(
    student_id bigint unsigned not null primary key auto_increment comment '主键',
    student_name varchar(64) not null comment '姓名',
    student_age tinyint unsigned not null default 18 comment '年龄',
    student_phone char(11) not null unique key comment '手机号',
    create_time datetime not null default now() comment '创建时间'
) engine=innodb charset=utf8mb4 comment '学生信息';
```

## 复制表结构

```sql
create table student_info_copy like student_info;
```
