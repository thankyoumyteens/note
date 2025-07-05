# 连接数据库

```py
import pymysql

# 建立连接
with pymysql.connect(
        host='127.0.0.1',  # 数据库地址
        port=3306,  # 端口号
        user='root',  # 用户名
        password='123456',  # 密码
        database='db_test',  # 数据库名
        charset='utf8mb4',  # 字符集
        cursorclass=pymysql.cursors.DictCursor  # 返回字典格式的结果
) as conn:
    print('ok')
```
