# 路由的基本定义

Flask 通过 @app.route() 装饰器定义路由，装饰器的参数为 URL 规则，被装饰的函数称为视图函数（View Function），负责处理请求并返回响应。

```py
# 根路径
@app.route('/')
def index():
    return '这是首页'

# 访问 /about 时触发
@app.route('/about')
def about():
    return '可以返回字符串、HTML、模板渲染结果等'
```
