# 拼接拆分路径

## 拼接路径

```python
from pathlib import Path

base_path = Path('/home')
# /home/user/bin/nginx
dist_path = base_path.joinpath('user', 'bin', 'nginx')
# 另一种写法
dist_path = base_path / 'user' / 'bin' / 'nginx'
```

## 拆分路径

```py
from pathlib import Path

base_path = Path('/home/user/bin/nginx')
# ('/', 'home', 'user', 'bin', 'nginx')
dist_path_tuple = base_path.parts

base_path = Path('c:\\Users\\Public')
# ('c:\\', 'Users', 'Public')
dist_path_tuple = base_path.parts
```
