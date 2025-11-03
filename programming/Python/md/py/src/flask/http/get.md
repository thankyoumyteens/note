# GET 请求

访问 `http://127.0.0.1:5000/search?query=python&page=3`

```py
from flask import Flask, request

app = Flask(__name__)

@app.route('/search')  # 默认支持 GET 方法
def search():
    # 获取 URL 中的 'query' 参数（如 /search?query=flask）
    query = request.args.get('query')
    # 如果参数不存在，返回default设置的默认值
    # 可以使用type明确指定类型为 int
    page = request.args.get('page', default=1, type=int)

    return f'查询内容：{query}，页码：{page}（类型：{type(page)}）'

if __name__ == '__main__':
    app.run(debug=True)
```

## 获取多个相同参数（如复选框）

例如 `http://example.com/select?tags=python&tags=flask`

```py
@app.route('/select')
def select():
    # 获取所有 'tags' 参数的值（返回列表）
    tags = request.args.getlist('tags')
    return f'选中的标签：{tags}'
```
