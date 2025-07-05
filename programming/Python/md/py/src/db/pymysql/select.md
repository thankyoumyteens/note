# 查询

```py
with conn.cursor() as cursor:
    # 执行 SQL 查询
    sql = "select * from test01 where id=%s"
    cursor.execute(sql, (1,))  # 参数化查询，防止 SQL 注入

    # 获取结果
    results = cursor.fetchall()
    for row in results:
        print(row)  # 打印每行数据(字典格式)
```
