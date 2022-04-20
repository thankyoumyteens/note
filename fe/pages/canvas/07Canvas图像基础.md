# drawImage(image, dx, dy, dw, dh)

* image: Image对象或canvas
* dx: 绘制的起始位置横坐标
* dy: 绘制的起始位置纵坐标
* dw和dh: 将图片按width和height进行缩放

# drawImage(image, sx, sy, sw, sh, dx, dy, dw, dh)

* 在图片上以(sx, sy)点为原点, 取宽sw高sh的矩形
* 将取到的矩形区域绘制到画布上以(dx, dy)点为原点的位置, 并根据dw和dh进行缩放

![](img/clipboard%20(36).png)

```
var image = new Image()
window.onload = function () {
    image.src = '1.jpg'
    image.onload = function () {
        context.drawImage(image, 
            300, 100, 200, 200,
            200, 200, 200, 200)
    }
}
```
![](img/clipboard%20(37).png)
