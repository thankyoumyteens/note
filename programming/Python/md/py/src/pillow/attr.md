# 获取图片属性

```py
from PIL import Image

im = Image.open('a.jpg')

# JPEG
print(im.format)
# (80, 80)
print(im.size)
# RGB
print(im.mode)
```

- format 代表图片文件的扩展名, 如果图片文件打开失败, 则其值为 None
- size 代表图片的大小, 以像素为单位, 使用包含两个元素的元组来返回
- mode 这个属性代表图片的 band 属性, 一般情况(黑白)下为 "L", 当图片是彩色的时候是 "RGB", 如果图片经过压缩, 则是 "CMYK"
