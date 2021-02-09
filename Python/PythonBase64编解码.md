# 将url编码成base64
```python
# 想将字符串转编码成base64,要先将字符串转换成二进制数据
url = "https://www.cnblogs.com/songzhixue/"
bytes_url = url.encode("utf-8")
# 被编码的参数必须是二进制数据
str_url = base64.b64encode(bytes_url)
print(str_url)

# b'aHR0cHM6Ly93d3cuY25ibG9ncy5jb20vc29uZ3poaXh1ZS8='
```
# 解码base64
```python
# 将base64解码成字符串
import base64
url = "aHR0cHM6Ly93d3cuY25ibG9ncy5jb20vc29uZ3poaXh1ZS8="
str_url = base64.b64decode(url).decode("utf-8")
print(str_url)

# 'https://www.cnblogs.com/songzhixue/'
```
