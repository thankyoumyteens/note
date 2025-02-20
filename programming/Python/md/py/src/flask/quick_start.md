# 基本使用

### 1. 安装

```sh
pip install Flask
pip install flask-cors
```

### 2. 使用

```py
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
# 跨域
cors = CORS(app, resources={r"/*": {"origins": "*"}})


@app.route('/userInfo', methods=['GET'])
def userInfo():
    return jsonify({
        'code': 0,
        'message': '操作成功',
        'data': 'Hello, World!'
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
```
