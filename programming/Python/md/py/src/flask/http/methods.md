# HTTP 方法限制

```py
from flask import request

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return '这是POST请求'
    else:
        return '这是GET请求'
```
