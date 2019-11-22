- <a href="#水平居中">水平居中</a>
- <a href="#垂直居中">垂直居中</a>
- <a href="#水平垂直居中">水平垂直居中</a>

<a id="水平居中"></a>
# 水平居中

## 内联元素水平居中

利用 text-align: center 可以实现在块级元素内部的内联元素水平居中。
此方法对内联元素(inline), 内联块(inline-block), 内联表(inline-table), 
inline-flex元素水平居中都有效。

```
.center-text {
    text-align: center;
}
```

## 块级元素水平居中

通过把固定宽度块级元素的margin-left和margin-right设成auto，就可以使块级元素水平居中。

```
.center-block {
  margin: 0 auto;
}
```

## 利用inline-block

如果一行中有两个或两个以上的块级元素，
通过设置块级元素的显示类型为inline-block和父容器的text-align属性从而使多块级元素水平居中。

```
.container {
    text-align: center;
}
.inline-block {
    display: inline-block;
}
```

<a id="垂直居中"></a>
# 垂直居中

## 单行内联(inline-)元素垂直居中

通过设置内联元素的高度(height)和行高(line-height)相等，从而使元素垂直居中。

```
#v-box {
    height: 120px;
    line-height: 120px;
}
```

## 利用表布局（table）

利用表布局的vertical-align: middle可以实现子元素的垂直居中。

```
.center-table {
    display: table;
}
.v-cell {
    display: table-cell;
    vertical-align: middle;
}
```

## 利用"精灵元素"

利用“精灵元素”(ghost element)技术实现垂直居中，
即在父容器内放一个100%高度的伪元素，
让文本和伪元素垂直对齐，从而达到垂直居中的目的。

```
.ghost-center {
    position: relative;
}
.ghost-center::before {
    content: " ";
    display: inline-block;
    height: 100%;
    width: 1%;
    vertical-align: middle;
}
.ghost-center p {
    display: inline-block;
    vertical-align: middle;
    width: 20rem;
}
```

## 块级元素垂直居中

### 固定高度的块级元素

我们知道居中元素的高度和宽度，垂直居中问题就很简单。
通过绝对定位元素距离顶部50%，并设置margin-top向上偏移元素高度的一半，
就可以实现垂直居中了。

```
.parent {
  position: relative;
}
.child {
  position: absolute;
  top: 50%;
  height: 100px;
  margin-top: -50px; 
}
```

### 未知高度的块级元素

当垂直居中的元素的高度和宽度未知时，
我们可以借助CSS3中的transform属性向Y轴反向偏移50%的方法实现垂直居中。
但是部分浏览器存在兼容性的问题。

```
.parent {
    position: relative;
}
.child {
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
}
```

<a id="水平垂直居中"></a>
# 水平垂直居中

## 固定宽高元素水平垂直居中

通过margin平移元素整体宽度的一半，使元素水平垂直居中。

```
.parent {
    position: relative;
}
.child {
    width: 300px;
    height: 100px;
    padding: 20px;
    position: absolute;
    top: 50%;
    left: 50%;
    margin: -70px 0 0 -170px;
}
```

## 未知宽高元素水平垂直居中

利用2D变换，在水平和垂直两个方向都向反向平移宽高的一半，从而使元素水平垂直居中。

```
.parent {
    position: relative;
}
.child {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
}
```

## 利用flex布局

利用flex布局，
其中justify-content 用于设置或检索弹性盒子元素在主轴（横轴）方向上的对齐方式；
而align-items属性定义flex子项在flex容器的当前行的侧轴（纵轴）方向上的对齐方式。

```
.parent {
    display: flex;
    justify-content: center;
    align-items: center;
}
```

## 利用grid布局
利用grid实现水平垂直居中，兼容性较差，不推荐。

```
.parent {
  height: 140px;
  display: grid;
}
.child { 
  margin: auto;
}
```

## 屏幕上水平垂直居中
屏幕上水平垂直居中十分常用，常规的登录及注册页面都需要用到。
要保证较好的兼容性，还需要用到表布局。

```
.outer {
    display: table;
    position: absolute;
    height: 100%;
    width: 100%;
}

.middle {
    display: table-cell;
    vertical-align: middle;
}

.inner {
    margin-left: auto;
    margin-right: auto; 
    width: 400px;
}
```
