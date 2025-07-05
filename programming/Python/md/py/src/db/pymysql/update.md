# 增删改

```py
with conn.cursor() as cursor:
    # 执行插入
    sql = "insert into test01 (id, name, msg, remark) VALUES (%s, %s, %s, %s)"
    cursor.execute(sql, (1, 'Alice', 'aaa', 'hahaha'))

# 提交事务
conn.commit()
```
