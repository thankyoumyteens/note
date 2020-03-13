# Python复制文件
```python
import shutil

#将指定的文件file复制到file_dir的文件夹里面
shutil.copy(file, file_dir)
```

# Python删除文件
```python
import os

# 不能删除目录
if(os.path.exists(dirPath+"foo.txt")):
　　os.remove(dirPath+"foo.txt")
```
