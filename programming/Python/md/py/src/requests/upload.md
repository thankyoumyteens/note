# 上传文件

```python
import requests

url = 'http://httpbin.org/post'
files = {
    'file': open('3.jpg', 'rb')
}
r = requests.post(url, files=files)
print(r.text)
```
