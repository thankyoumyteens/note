# import 绝对路径

```python
import sys
import os
from pathlib import Path

# 当前文件所在的文件夹
dist_path = Path(os.path.abspath(os.path.dirname(__file__)))
# 要导入的文件所在的文件夹
utils_path = dist_path.parent / 'utils'
# 添加到path
sys.path.append(str(mybatis_generator_path))
# 导入
from utils import MyUtil

print(MyUtil().test())
```
