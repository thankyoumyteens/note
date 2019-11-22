# 绘制圆弧

```
context.arc(
centerX, centerY,  // 圆心的坐标
radius, // 圆弧的半径
startingAngle, // 开始的角度
endingAngle, // 结束的角度
anticlockwise = false // 是否逆时针绘制
)
```
* startingAngle和endingAngle的取值如下图
* 不管anticlockwise取值是什么它们始终是顺时针的
![](img/clipboard%20(22).png)
## 示例
* 顺时针
```
for(var i = 0; i < 10; i++) {
    context.beginPath()
    // startingAngle不变
    // 逐渐增加endingAngle
    context.arc(50 + i * 100, 60, 40,
        0, 2 * Math.PI * (i + 1) / 10)
    context.stroke()
}
```
![](img/clipboard%20(23).png)
```
for(var i = 0; i < 10; i++) {
    context.beginPath()
    context.arc(50 + i * 100, 180, 40,
        0, 2 * Math.PI * (i + 1) / 10)
    // 连接起始点和终止点
    context.closePath()
    context.stroke()
}
```
![](img/clipboard%20(24).png)
* 逆时针
```
for(var i = 0; i < 10; i++) {
    context.beginPath()
    context.arc(50 + i * 100, 420, 40,
        0, 2 * Math.PI * (i + 1) / 10,
        true)
    context.stroke()
}
```
![](img/clipboard%20(25).png)
```
for(var i = 0; i < 10; i++) {
    context.beginPath()
    context.arc(50 + i * 100, 300, 40,
        0, 2 * Math.PI * (i + 1) / 10,
        true)
    context.closePath()
    context.stroke()
}
```
![](img/clipboard%20(26).png)

# 绘制圆角矩形

![](img/clipboard%20(27).png)
```
drawRoundRect(context, 100, 100, 600, 500, 50)

function drawRoundRect(cxt, x, y, width, height, radius) {
    cxt.save()
    cxt.translate(x, y)
    pathRoundRect(cxt, width, height, radius)
    cxt.strokeStyle = 'black'
    cxt.stroke()
    cxt.restore()
}

function pathRoundRect(cxt, width, height, radius) {
    cxt.beginPath()
    // 从右下角开始绘制, 顺时针, 绘制到右上角结束
    cxt.arc(width - radius, height - radius, radius, 0, Math.PI / 2)
    cxt.lineTo(radius, height)
    cxt.arc(radius, height - radius, radius, Math.PI / 2, Math.PI)
    cxt.lineTo(0, radius)
    cxt.arc(radius, radius, radius, Math.PI, Math.PI * 3 / 2)
    cxt.lineTo(width - radius, 0)
    cxt.arc(width - radius, radius, radius, Math.PI * 3 / 2, Math.PI * 2)
    cxt.closePath()
}
```

# 绘制圆弧
* moveTo(x0, y0)
* arcTo(x1, y1, x2, y2, radius)
![](img/clipboard%20(28).png)
```
context.beginPath()
context.moveTo(150, 150) // (x0, y0)
context.arcTo(650, 150, 650, 650, 500)
context.lineWidth = 6
context.strokeStyle = 'red'
context.stroke()
// 辅助线
context.beginPath()
context.moveTo(150, 150)
context.lineTo(650, 150)
context.lineTo(650, 650)
context.lineWidth = 2
context.strokeStyle = 'gray'
context.stroke()
```

# 贝塞尔曲线

## 二次贝塞尔曲线
* moveTo(x0, y0)
* quadraticCurveTo(x1, y1, x2, y2)
![](img/clipboard%20(29).png)

## 三次贝塞尔曲线
* moveTo(x0, y0)
* bezierCurveTo(x1, y1, x2, y2, x3, y3)
![](img/clipboard%20(30).png)
