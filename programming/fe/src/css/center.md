# 居中

## 水平居中

前提: 父元素宽度确定

将 margin-left 和 margin-right 属性设置为 auto, 从而达到水平居中的效果

```css
.demo {
  margin: 0 auto;
}
```

## 水平垂直居中

前提: display 为 inline 或 inline-block, 父元素高度确定

- 水平居中: 将 text-align 设为 center
- 垂直居中: 将 line-height 设为和 height 一样

```css
.parent {
  text-align: center;
  line-height: 200px;
  height: 200px;
}

.children {
  display: inline-block;
}
```

## absolute+transform 居中

前提: 父元素高度确定

```css
.parent {
  position: relative;
  width: 100%;
  height: 200px;
  background-color: red;
}

.children {
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  height: 50px;
  width: 50px;
  background-color: black;
}
```

## absolute+margin 居中

前提: 父元素宽度和高度确定

```css
.parent {
  position: relative;
  width: 200px;
  height: 200px;
  background-color: red;
}

.children {
  position: absolute;
  left: 50%;
  top: 50%;
  margin: -25px 0 0 -25px;
  height: 50px;
  width: 50px;
  background-color: black;
}
```

## flex 居中

```css
.parent {
  display: flex;
  align-items: center; /*垂直居中*/
  justify-content: center; /*水平居中*/
  width: 100%;
  height: 100%;
  background-color: red;
}

.children {
  background-color: blue;
}
```
