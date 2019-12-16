# Python判断文件还是文件夹

```
import os

if os.path.isdir(path):
    print "文件夹"
elif os.path.isfile(path):
    print "文件"
else:
    print "socket,FIFO,device"
```
