# Java使用poi-tl动态渲染word模板时图像变红

使用poi-tl动态渲染word模板时发现有的图片会变红，检查代码发现有这么一行

```java
PictureRenderData pic = Pictures.ofBufferedImage(image, PictureType.JPEG).size(300, 200).create();
```

## 原因

网上找了一下，找到一个可能的原因：ImageIO.read()方法读取图片时可能存在不正确处理图片ICC信息的问题，导致渲染图片前景色时蒙上一层红色。ICC为JPEG图片格式中的一种头部信息，里面有参数告诉显示器用什么色域来显示图像。

Pictures.ofBufferedImage()方法里面确实用到了ImageIO.read()方法。

## 解决方案

改成png：

```java
PictureRenderData pic = Pictures.ofBufferedImage(image, PictureType.PNG).size(300, 200).create();
```
