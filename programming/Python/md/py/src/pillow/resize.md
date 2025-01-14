# 缩放图片

```py
from PIL import Image

im = Image.open('1.jpg')

# 调整图像大小
im = im.resize((800, 600))

im.save('dst.jpg')
```
