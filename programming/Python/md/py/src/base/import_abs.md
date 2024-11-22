# import 绝对路径

```
.
├── utils
│   └── my_util.py
└── my_module
    └── main.py
```

在 main.py 中导入 my_util.py 的类:

```python
import sys
import os
from pathlib import Path

# 当前文件所在的文件夹
dist_path = Path(os.path.abspath(os.path.dirname(__file__)))
# 要导入的文件所在的文件夹
utils_path = dist_path.parent / 'utils'
# 添加到path
sys.path.append(str(utils_path))
# 导入
from my_util import MyUtil

print(MyUtil().test())
```
