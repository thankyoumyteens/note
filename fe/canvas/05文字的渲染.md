# 写一行文字

* font = 'bold 40px Arial'
* fillText(string, x, y, \[最大宽度\])
* strokeText(string, x, y, \[最大宽度\])
```
context.font = 'bold 40px Arial'
var linear = context.createLinearGradient(0, 0, 100, 0)
linear.addColorStop(0.0, 'blue')
linear.addColorStop(1.0, 'green')
context.fillStyle = linear
context.strokeStyle = '#058'
context.lineWidth = 1
context.fillText('你好', 40, 100)
context.strokeText('你好', 40, 200)
context.strokeText('你好', 40, 300, 50)
```
![](img/clipboard%20(31).png)

# 文本对齐

* textAlign = left | right | center
* textBaseline = top | middle | bottom
```
context.font = 'bold 40px Arial'
context.fillStyle = '#058'

context.textAlign = 'left'
context.fillText('你好', 400, 100)
context.textAlign = 'center'
context.fillText('你好', 400, 200)
context.textAlign = 'right'
context.fillText('你好', 400, 300)
// 辅助线
context.strokeStyle = '#888'
context.moveTo(400, 0)
context.lineTo(400, 800)
context.stroke()
```
![](img/clipboard%20(32).png)

# 文本的度量
```
// 返回string实际渲染的宽度
context.measureText(string).width
```
