# URL 嵌入参数

```py
@app.route('/user/<username>')  # <username> 是动态参数
def show_user(username):  # 视图函数必须接收该参数
    return f'欢迎，{username}！'
```

访问 `http://127.0.0.1:5000/user/张三` 时，username 会被赋值为 '张三'，页面显示 欢迎，张三！。

## 转换器

默认情况下，动态参数会被当作字符串处理。Flask 支持通过转换器限制参数类型，语法为 `<转换器:参数名>`。常用转换器：

- string：默认类型，接受除 `/` 外的任何字符（可省略）
- int：仅接受整数
- float：仅接受浮点数
- path：类似 string，但允许包含 `/`（适合匹配路径）
- uuid：仅接受 UUID 字符串（如 a1b2c3d4-5678-90ef-ghij-klmnopqrstuv）

```py
# 仅接受整数 ID
@app.route('/post/<int:post_id>')
def show_post(post_id):
    # 输出：文章 ID：123（类型：<class 'int'>）
    return f'文章 ID：{post_id}（类型：{type(post_id)}）'

# 接受带 / 的路径（如 /file/docs/readme.txt）
@app.route('/file/<path:file_path>')
def show_file(file_path):
    # 访问 /file/docs/readme.txt 时，输出：文件路径：docs/readme.txt
    return f'文件路径：{file_path}'

# 仅接受 UUID
@app.route('/item/<uuid:item_id>')
def show_item(item_id):
    # 仅匹配 UUID 格式，如 /item/123e4567-e89b-12d3-a456-426614174000
    return f'物品 UUID：{item_id}'
```

如果参数类型不匹配（如访问 /post/abc 时，abc 不是整数），Flask 会返回 404 Not Found。
