# 获取当前路径

## 获取当前 python 文件所在的路径

```python
import os

dist_path = os.path.abspath(os.path.dirname(__file__))
```

## 获取当前当前登录用户的家路径

```python
from pathlib import Path

home_path = Path.home()
```

## 获取当前当前工作目录的路径

```python
from pathlib import Path

work_path = Path.cwd()
```
