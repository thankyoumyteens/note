# 路径转换

## 相对路径转绝对路径

```python
from pathlib import Path

# 传入相对路径(相对于工作目录)
relative_path = Path('a.txt')
# 获取绝对路径
absolute_path = relative_path.resolve()
```

## 绝对路径转相对路径

```python
from pathlib import Path

# 传入绝对路径
absolute_path = Path('/home/demo/a.txt')
# 获取相对/home/demo的路径: a.txt
relative_path = absolute_path.relative_to('/home/demo')
```
