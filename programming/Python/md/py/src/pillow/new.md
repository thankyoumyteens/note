# 新建图片

```py
from PIL import Image

# 创建一个新的图像
# 模式：RGB
# 大小：800x600
# 颜色：(255, 255, 255)
im = Image.new('RGB', (800, 600), (255, 255, 255))
# 保存图像
im.save('dst.jpg')
```
