# 路径操作

## 获取上级目录/文件名/扩展名

```py
from pathlib import Path

base_path = Path('/home/demo.txt')
# .txt
file_suffix = base_path.suffix
# demo.txt
file_name = base_path.name
# demo
file_stem = base_path.stem
# /home
file_parent = base_path.parent
```

## 获取 windows 盘符

```py
from pathlib import Path

base_path = Path('c:\\Users\\Public')
# c:
dist_drive = base_path.drive
```

## 创建多级文件夹

- parents = True: 创建中间级父目录
- exist_ok= True: 目标目录存在时不报错

```python
from pathlib import Path

base_path = Path('/home/demo1/demo2')
base_path.mkdir(parents=True, exist_ok=True)
```

## 判断文件或文件夹是否存在

```python
from pathlib import Path

src_path = Path('/home/demo1/1.txt')
# 返回布尔值
src_path.exists()

src_path = Path('/home/demo1')
src_path.exists()
```

## 判断是不是文件

```python
from pathlib import Path

src_path = Path('/home/demo1/1.txt')
# 返回布尔值
src_path.is_file()
```

## 判断是不是文件夹

```python
from pathlib import Path

src_path = Path('/home/demo1')
# 返回布尔值
src_path.is_dir()
```
