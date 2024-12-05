# 重命名

```python
from pathlib import Path

src_path = Path('/home/demo1/1.txt')
# 重命名文件
src_path.rename('/home/demo1/2.txt')

src_path = Path('/home/demo1')
# 重命名文件夹
src_path.rename('/home/demo2')
```
