# 旋转

```py
from PIL import Image

im = Image.open('1.jpg')

# 逆时针旋转90度
im = im.rotate(90)

im.save('dst.jpg')
```
