# 基本使用

```py
from flask import Flask

# 初始化 Flask 应用，__name__ 表示当前模块名
app = Flask(__name__)


# 定义路由：访问根路径 '/' 时触发该函数
@app.route('/')
def hello_world():
    return 'Hello, Flask!'


# 启动服务器（仅在直接运行该脚本时执行）
if __name__ == '__main__':
    app.run(debug=True)  # debug=True 开启调试模式，代码修改后自动重启
```
