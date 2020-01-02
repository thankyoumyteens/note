# Python复制文件

```
import shutil

#将指定的文件file复制到file_dir的文件夹里面
shutil.copy(file, file_dir)
```

# Python删除文件

`os.remove()`方法用于删除指定路径的文件, 如果指定的路径是一个目录, 将抛出OSError

```
import os

if(os.path.exists(dirPath+"foo.txt")):
　　os.remove(dirPath+"foo.txt")
```
