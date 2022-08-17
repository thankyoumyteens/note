# 无参数

```python
import requests

# timeout 设置超时
r = requests.get('http://localhost:8080/test', timeout=0.001)
# HTTP状态码
print(r.status_code)
# Requests 会基于 HTTP 头部对响应的编码作出有根据的推测
# 当访问 r.text 之时，Requests 会使用其推测的文本编码
# 可以使用 r.encoding 属性指定编码
r.encoding = 'utf-8'
print(r.text)
```

# 有参数

```python
import requests

r = requests.get('http://localhost:8080/test', params={
    'key1': 'value1',
    'key2': 'value2'
})
# 响应体 JSON 解码
print(r.json())
```
