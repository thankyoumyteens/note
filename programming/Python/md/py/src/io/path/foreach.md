# 遍历目录

## 获取直接下级文件和文件夹

```python
from pathlib import Path

base_path = Path('/home')

# 获取直接下级文件和文件夹
for path_obj in base_path.iterdir():
    # /home/demo
    # /home/1.txt
    print(str(path_obj))
```

## 获取所有下级文件和文件夹

```python
from pathlib import Path

base_path = Path('/home')

# 获取所有下级文件和文件夹
for path_obj in base_path.glob("**/*"):
    # /home/demo
    # /home/demo/2.txt
    # /home/1.txt
    print(str(path_obj))
```

## 获取当前文件夹下的指定文件

```python
from pathlib import Path

base_path = Path('/home')

# 获取当前文件夹下的所有mp4文件
for path_obj in base_path.glob("*.mp4"):
    print(str(path_obj))
```
