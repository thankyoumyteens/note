# 转换图片格式

```py
im = Image.open('a.jpg')
# 转成png
im.save('a.png')
```

如果文件名中的后缀不是标准的扩展名, save 函数需要手动传入 format 参数来指定图片的扩展名。
