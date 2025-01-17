# 翻转

```py
from PIL import Image

im = Image.open('1.jpg')

# 左右翻转
im = im.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
# 上下翻转
im = im.transpose(Image.Transpose.FLIP_TOP_BOTTOM)

im.save('dst.jpg')
```
