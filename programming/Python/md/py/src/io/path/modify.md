# 复制移到删除

## 复制文件

```python
from pathlib import Path
import shutil

src_path = Path('/home/demo1/1.txt')
dest_path = Path('/home/demo2/1_copy.txt')
shutil.copyfile(str(src_path), str(dest_path))
```

## 复制文件夹

```python
from pathlib import Path
import shutil

src_path = Path('/home/demo1')
dest_path = Path('/home/demo2')
# 递归复制demo1文件夹到新创建的demo2文件夹
# 若demo2文件夹存在则报错
shutil.copytree(str(src_path), str(dest_path))
```

## 移动文件

```python
from pathlib import Path

src_path = Path('/home/demo1/1.txt')
dest_path = Path('/home/demo2/2.txt')
# 如果2.txt已存在会被覆盖
src_path.replace(dest_path)
```

## 移动文件夹

```python
from pathlib import Path
import shutil

src_path = Path('/home/demo1')
dest_path = Path('/home/demo2')
# 移动整个demo1文件夹到demo2文件夹下
shutil.move(str(src_path), str(dest_path))
```

## 删除文件

```python
from pathlib import Path

src_path = Path('/home/demo1/1.txt')
src_path.unlink()
```

## 删除文件夹

```python
from pathlib import Path
import shutil

src_path = Path('/home/demo1')
# 删除文件夹及其下所有文件
shutil.rmtree(str(src_path))
```
