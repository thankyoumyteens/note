# 获取请求头

```py
from flask import Flask, request

app = Flask(__name__)

@app.route('/headers')
def get_headers():
    # 获取常见请求头
    user_agent = request.headers.get('User-Agent')  # 客户端浏览器/设备信息
    content_type = request.headers.get('Content-Type')  # 请求体类型
    accept = request.headers.get('Accept')  # 客户端可接受的响应类型

    return f'''
        User-Agent: {user_agent}<br>
        Content-Type: {content_type}<br>
        Accept: {accept}
    '''

if __name__ == '__main__':
    app.run(debug=True)
```

## 遍历所有请求头

```py
@app.route('/all_headers')
def all_headers():
    headers = []
    for key, value in request.headers.items():
        headers.append(f'{key}: {value}')
    return '<br>'.join(headers)
```
