# POST 请求

## 接收表单数据

```py
from flask import Flask, request

app = Flask(__name__)

@app.route('/register', methods=['POST'])
def register():
    # 提取表单数据
    username = request.form.get('username')  # 获取用户名
    password = request.form.get('password')  # 获取密码
    hobbies = request.form.getlist('hobby')  # 获取复选框的多个值

    return f'''
        注册信息：<br>
        用户名：{username}<br>
        密码：{password}<br>
        爱好：{hobbies}
    '''

if __name__ == '__main__':
    app.run(debug=True)
```

## 接收 JSON 数据

```py
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/user', methods=['POST'])
def add_user():
    # 解析 JSON 数据（若请求头不是 application/json，返回 None）
    data = request.get_json()

    if not data:
        # 400 表示请求错误
        return jsonify({'error': '请发送 JSON 数据'}), 400

    # 提取 JSON 中的字段
    username = data.get('username')
    age = data.get('age')

    return jsonify({
        'status': 'success',
        'message': f'用户 {username}（年龄 {age}）已添加'
    })

if __name__ == '__main__':
    app.run(debug=True)
```

## 文件上传

文件上传的表单需指定 `enctype="multipart/form-data"`，此时使用 request.files 提取文件。

```py
from flask import Flask, request

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_file():
    # 获取上传的文件（name 属性为 'file'）
    file = request.files['file']

    if file.filename == '':  # 未选择文件
        return '未选择文件'

    # 保存文件到本地（如 static 文件夹）
    file.save(f'static/{file.filename}')
    return f'文件 {file.filename} 上传成功'

if __name__ == '__main__':
    app.run(debug=True)
```
