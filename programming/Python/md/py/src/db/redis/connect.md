# 连接 redis

```py
import redis

# 连接到 Redis
connection = redis.Redis(
    host='localhost',
    port=6379,
    db=0,
    password='your_password_here',  # 添加密码参数
    decode_responses=True
)
```
