# 线性渐变

* 定义一条渐变线: createLinearGradient(xStart, yStart, xEnd, yEnd)
```
var linearGrad = context.createLinearGradient(0, 0, 400, 400)
linearGrad.addColorStop(0.0, 'white')
linearGrad.addColorStop(0.25, 'yellow')
linearGrad.addColorStop(0.5, 'green')
linearGrad.addColorStop(0.75, 'blue')
linearGrad.addColorStop(1.0, 'black')
context.fillStyle = linearGrad
context.fillRect(0, 0, 800, 800)
```
![](img/clipboard%20(19).png)

# 径向渐变

* 定义两个圆环: createRadialGradient(x0, y0, r0, x1, y1, r1)
```
var radialGrad = context.createRadialGradient(400, 400, 100, 400, 400, 500)
radialGrad.addColorStop(0.0, 'white')
radialGrad.addColorStop(0.25, 'yellow')
radialGrad.addColorStop(0.5, 'green')
radialGrad.addColorStop(0.75, 'blue')
radialGrad.addColorStop(1.0, 'black')
context.fillStyle = radialGrad
context.fillRect(0, 0, 800, 800)
```
![](img/clipboard%20(20).png)

# 使用图片填充

```
var img = new Image()
img.src = '1.jpg'
img.onload = function () {
    var pattern = context.createPattern(img, 'repeat-y')
    context.fillStyle = pattern
    context.fillRect(0, 0, 800, 800)
}
```
![](img/clipboard%20(21).png)
