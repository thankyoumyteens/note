# 复制和粘贴矩形区域

## 把矩形区域保存成新图片

```py
from PIL import Image

im = Image.open('1.jpg')
region = im.crop((1000, 1000, 1400, 1400))
# 把region保存成新图片
region.save('dst.jpg')
```

## 把矩形区域粘贴到原图片

```py
from PIL import Image

im = Image.open('1.jpg')

# 把 (1000, 1000) 位置的 400*400 大小的图片复制到 (1, 1) 位置

# 元组: 左上右下的坐标
region = im.crop((1000, 1000, 1400, 1400))
# 把region粘贴到(1, 1)位置
im.paste(region, (1, 1))

im.save('dst.jpg')
```

## 把矩形区域粘贴到另一张图片

```py
im = Image.open('1.jpg')
im2 = Image.open('2.jpg')

region = im.crop((1000, 1000, 1400, 1400))
# 把region粘贴到另一张图片
im2.paste(region, (1, 1))

im2.save('dst.jpg')
```
