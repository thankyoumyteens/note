# css 的选择器权重比较以及权重计算规则

CSS 优先级的计算规则如下：

- 元素标签中定义的样式（Style 属性）,加 1,0,0,0
- 每个 ID 选择符(如 #id),加 0,1,0,0
- 每个 Class 选择符(如 .class).每个属性选择符(如 [attribute=]).每个伪类(如 :hover)加 0,0,1,0
- 每个元素选择符（如 p）或伪元素选择符(如 :first-child)等，加 0,0,0,1
  然后，将这四个数字分别累加，就得到每个 CSS 定义的优先级的值，
  然后从左到右逐位比较大小，数字大的 CSS 样式的优先级就高。
  1,0,0,0 > 0,99,99,99。也就是说从左往右逐个等级比较，前一等级相等才往后比。
  例子：
  css 文件或`<style>`中如下定义：

1.  h1 {color: red;}
    /_ 一个元素选择符，结果是 0,0,0,1 _/
2.  body h1 {color: green;}
    /_ 两个元素选择符，结果是 0,0,0,2 _/
3.  h2.grape {color: purple;}
    /_ 一个元素选择符.一个 Class 选择符，结果是 0,0,1,1_/
4.  li#answer {color: navy;}
    /_ 一个元素选择符，一个 ID 选择符，结果是 0,1,0,1 _/
    元素的 style 属性中如下定义：
    h1 {color: blue;}
    /_ 元素标签中定义，一个元素选择符，结果是 1,0,0,1_/

如此以来，h1 元素的颜色是蓝色。
注意：
1.!important 声明的样式优先级最高，如果冲突再进行计算。 2.如果优先级相同，则选择最后出现的样式。 3.继承得到的样式的优先级最低。

结论是：比较同一级别的个数，数量多的优先级高，如果相同即比较下一级别的个数
important->内联->ID->类->标签|伪类|属性选择->伪对象->继承->通配符->继承

最后汇总为一张表

| 选择器         | 表达式或示例      | 权重                   |
| -------------- | ----------------- | ---------------------- |
| ID 选择器      | #aaa              | 100                    |
| 类选择器       | .aaa              | 10                     |
| 标签选择器     | h1                | 1                      |
| 属性选择器     | [title]           | 10                     |
| 相邻选择器     | selecter+selecter | 拆分为两个选择器再计算 |
| 兄长选择器     | selecter~selecter | 拆分为两个选择器再计算 |
| 父子选择器     | selecter>selecter | 拆分为两个选择器再计算 |
| 后代选择器     | selecter selecter | 拆分为两个选择器再计算 |
| 通配符         | \*                | 0                      |
| 各种伪类选择器 | :hover            | 10                     |
| 各种伪元素     | ::after           | 1                      |

# display 有哪几种值，分别是什么意思

1.  none 此元素不会被显示，并且不占据页面空间，这也是与 visibility:hidden 不同的地方，设置 visibility:hidden 的元素，不会被显示，但是还是会占据原来的页面空间
2.  inline 行内元素 元素会在一行内显示，超出屏幕宽度自动换行，不能设置宽度和高度，元素的宽度和高度只能是靠元素内的内容撑开
3.  block 块级元素 会独占一行，如果不设置宽度，其宽度会自动填满父元素的宽度，可以设置宽高，即使设置的宽度小于父元素的宽度，块级元素也会独占一行
4.  inline-block 行内块元素 与行内元素一样可以在一行内显示，而且可以设置宽高，可以设置 margin 和 padding
5.  list-item 列表元素
6.  table 会作为块级表格来显示(类似于`<table>`)，表格前后带有换行符
7.  inline-table 会作为内联表格来显示(类似于`<table>`)，表格前后没有换行符
8.  table-cell 会作为表格单元格来显示(类似于`<td>`)
9.  flex 多栏多列布局

# 常用的块级元素

div、p、h1~h6、ul、ol、dl、li、dd、table、hr、HTML5新增的header、section、aside、footer

# 常用的行内元素

span、img、a、label、input、textarea、select、button

# 替换元素
  替换元素根据其标签和属性来决定元素的具体显示内容.有img input textarea select object。
  替换一般有内在尺寸即img默认的是其图片的宽高，input也有默认的尺寸。img和input的宽高可以设定。

# text-decoration 分别有哪几种值

1.  text-decoration:none //默认，定义标准的文本，没有任何样式，正常显示
2.  text-decoration:underline //定义文本下的一条线
3.  text-decoration:overline //定义文本上的一条线
4.  text-decoration:line-through //定义文本中间的一条线

# 标准盒模型和 IE 盒模型

![w3c](img/w3cbox.jpg)

![ie](img/iebox.jpg)

# box-sizing

1. content-box: 默认值, 让元素维持W3C盒模型
2. border-box 让元素维持IE盒模型

# BFC(Block Formatting Context, 块格式化上下文)

BFC 的创建方法

- 根元素或其它包含它的元素；
- 浮动 (元素的 float 不为 none)；
- 绝对定位元素 (元素的 position 为 absolute 或 fixed)；
- 行内块 inline-blocks(元素的 display: inline-block)；
- 表格单元格(元素的 display: table-cell，HTML 表格单元格默认属性)；
- overflow 的值不为 visible 的元素；
- 弹性盒 flex boxes (元素的 display: flex 或 inline-flex)；

BFC 的效果

- 内部的盒会在垂直方向一个接一个排列（可以看作 BFC 中有一个的常规流）；
- 处于同一个 BFC 中的元素相互影响，可能会发生 margin collapse；
- 每个元素的 margin box 的左边，与容器块 border box 的左边相接触(对于从左\* 往右的格式化，否则相反) 即使存在浮动也是如此；
- BFC 就是页面上的一个隔离的独立容器，容器里面的子元素不会影响到外面的元素，反之亦然；
- 计算 BFC 的高度时，考虑 BFC 所包含的所有元素，连浮动元素也参与计算；
- 浮动盒区域不叠加到 BFC 上；

# 垂直 margin 的合并

垂直 margin 合并就是上下相邻的两个块级元素，如果刚好，上面设置 margin-bottom，下面设置 margin-top，这俩外边距相遇了，那两个就合并了，本来可能上面 margin-bottom 设置 20px，margin-top 设置 10px，合并之后两个元素上下的距离就变为 20px，即两个属性中较大的值

垂直 margin 合并是在同一个 BFC 中才会发生的，如果两个 BFC 的垂直 margin 不会合并

# 垂直水平居中

> 元素水平居中

```
// 元素需要设置宽度
// 不是行内元素
margin: 0 auto;
```

> 元素水平垂直居中

方案 1：position 元素已知宽度
父元素设置为：position: relative;
子元素设置为：position: absolute;
距上 50%，据左 50%，然后减去元素自身宽度的距离就可以实现

```
<div class="box">
    <div class="content"></div>
</div>

.box {
    width: 300px;
    height: 300px;
    position: relative;
}
.content {
    width: 100px;
    height: 100px;
    position: absolute;
    left: 50%;
    top: 50%;
    margin: -50px 0 0 -50px;
}
```

方案 2：position transform 元素未知宽度
如果元素未知宽度，只需将上面例子中的 margin: -50px 0 0 -50px;替换为：transform: translate(-50%,-50%);

```
<div class="box">
    <div class="content"></div>
</div>

.box {
    width: 300px;
    height: 300px;
    position: relative;
}
.content {
    position: absolute;
    left: 50%;
    top: 50%;
    transform: translate(-50%,-50%);
}
```

方案 3：flex 布局

```
<div class="box">
    <div class="content"></div>
</div>

.box {
    width: 300px;
    height: 300px;
    display: flex;//flex布局
    justify-content: center;//使子项目水平居中
    align-items: center;//使子项目垂直居中
}
.content {
    width: 100px;
    height: 100px;
}
```

方案 4：table-cell 布局
因为 table-cell 相当与表格的 td，td 为行内元素，无法设置宽和高，所以嵌套一层，嵌套一层必须设置 display: inline-block;td 的背景覆盖了橘黄色，不推荐使用

```
<div class="box">
    <div class="content">
        <div class="inner"></div>
    </div>
</div>

.box {
    background-color: #FF8C00;//橘黄色
    width: 300px;
    height: 300px;
    display: table;
}
.content {
    background-color: #F00;//红色
    display: table-cell;
    vertical-align: middle;//使子元素垂直居中
    text-align: center;//使子元素水平居中
}
.inner {
    background-color: #000;//黑色
    display: inline-block;
    width: 20%;
    height: 20%;
}
```

# 负边距

todo

# CSS Hack

todo
