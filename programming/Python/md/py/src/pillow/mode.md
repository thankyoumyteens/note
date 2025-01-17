# 颜色

支持每个格式与 L 和 RGB 的相互转换

```py
from PIL import Image

im = Image.open('1.jpg')

# 黑白色
im = im.convert('L')

im.save('dst.jpg')
```
