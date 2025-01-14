# 打开图片

```py
from PIL import Image

im = Image.open('/Users/walter/Downloads/1.jpg')
# 首先将图像保存到一个临时文件中，然后调用系统默认打开图像的程序来加载这个临时文件
im.show()
```
