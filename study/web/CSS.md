# CSS 选择器

| 选择器               | 例子                  | 例子描述                                          | CSS |
| -------------------- | --------------------- | ------------------------------------------------- | --- |
| .class               | .intro                | 选择 class="intro" 的所有元素                     | 1   |
| #id                  | #firstname            | 选择 id="firstname" 的所有元素                    | 1   |
| \*                   | \*                    | 选择所有元素                                      | 2   |
| element              | p                     | 选择所有`<p>`元素                                 | 1   |
| element,element      | div,p                 | 选择所有`<div>`元素和所有`<p>`元素                | 1   |
| element element      | div p                 | 选择`<div>`元素内部的所有`<p>`元素                | 1   |
| element>element      | div>p                 | 选择父元素为`<div>`元素的所有`<p>`元素            | 2   |
| element+element      | div+p                 | 选择紧接在`<div>`元素之后的所有`<p>`元素          | 2   |
| [attribute]          | [target]              | 选择带有 target 属性所有元素                      | 2   |
| [attribute=value]    | [target=_blank]       | 选择 target="\_blank" 的所有元素                  | 2   |
| [attribute~=value]   | [title~=flower]       | 选择 title 属性包含单词 "flower" 的所有元素       | 2   |
| [attribute\|=value]  | [lang\|=en]           | 选择 lang 属性值以 "en" 开头的所有元素            | 2   |
| :link                | a:link                | 选择所有未被访问的链接                            | 1   |
| :visited             | a:visited             | 选择所有已被访问的链接                            | 1   |
| :active              | a:active              | 选择活动链接                                      | 1   |
| :hover               | a:hover               | 选择鼠标指针位于其上的链接                        | 1   |
| :focus               | input:focus           | 选择获得焦点的 input 元素                         | 2   |
| :first-letter        | p:first-letter        | 选择每个`<p>`元素的首字母                         | 1   |
| :first-line          | p:first-line          | 选择每个`<p>`元素的首行                           | 1   |
| :first-child         | p:first-child         | 选择属于父元素的第一个子元素的每个`<p>`元素       | 2   |
| :before              | p:before              | 在每个`<p>`元素的内容之前插入内容                 | 2   |
| :after               | p:after               | 在每个`<p>`元素的内容之后插入内容                 | 2   |
| :lang(language)      | p:lang(it)            | 选择带有以 "it" 开头的 lang 属性值的每个`<p>`元素 | 2   |
| element1~element2    | p~ul                  | 选择前面有`<p>`元素的每个`<ul>`元素               | 3   |
| [attribute^=value]   | a[src^="https"]       | 选择其 src 属性值以 "https" 开头的每个`<a>`元素   | 3   |
| [attribute$=value]   | a[src$=".pdf"]        | 选择其 src 属性以 ".pdf" 结尾的所有`<a>`元素      | 3   |
| [attribute*=value]   | a[src*="abc"]         | 选择其 src 属性中包含 "abc" 子串的每个`<a>`元素   | 3   |
| :first-of-type       | p:first-of-type       | 选择属于其父元素的首个 `<p>`元素的每个 `<p>`元素  | 3   |
| :last-of-type        | p:last-of-type        | 选择属于其父元素的最后 `<p>`元素的每个 `<p>`元素  | 3   |
| :only-of-type        | p:only-of-type        | 选择属于其父元素唯一的 `<p>`元素的每个 `<p>`元素  | 3   |
| :only-child          | p:only-child          | 选择属于其父元素的唯一子元素的每个 `<p>`元素      | 3   |
| :nth-child(n)        | p:nth-child(2)        | 选择属于其父元素的第二个子元素的每个 `<p>`元素    | 3   |
| :nth-last-child(n)   | p:nth-last-child(2)   | 同上，从最后一个子元素开始计数                    | 3   |
| :nth-of-type(n)      | p:nth-of-type(2)      | 选择属于其父元素第二个 `<p>`元素的每个 `<p>`元素  | 3   |
| :nth-last-of-type(n) | p:nth-last-of-type(2) | 同上，但是从最后一个子元素开始计数                | 3   |
| :last-child          | p:last-child          | 选择属于其父元素最后一个子元素每个 `<p>`元素      | 3   |
| :root                | :root                 | 选择文档的根元素                                  | 3   |
| :empty               | p:empty               | 选择没有子元素的每个 `<p>`元素（包括文本节点）    | 3   |
| :target              | #news:target          | 选择当前活动的 #news 元素                         | 3   |
| :enabled             | input:enabled         | 选择每个启用的`<input>`元素                       | 3   |
| :disabled            | input:disabled        | 选择每个禁用的`<input>`元素                       | 3   |
| :checked             | input:checked         | 选择每个被选中的`<input>`元素                     | 3   |
| :not(selector)       | :not(p)               | 选择非 `<p>`元素的每个元素                        | 3   |
| ::selection          | ::selection           | 选择被用户选取的元素部分                          | 3   |

# css 的选择器权重比较以及权重计算规则

CSS 优先级的计算规则如下：

- 元素标签中定义的样式（Style 属性）,加 1,0,0,0
- 每个 ID 选择符(如 #id),加 0,1,0,0
- 每个 Class 选择符(如 .class).每个属性选择符(如 [attribute=]).每个伪类(如 :hover)加 0,0,1,0
- 每个元素选择符（如 p）或伪元素选择符(如 :firstchild)等，加 0,0,0,1
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
3.  block 块级元素 会独占一行，如果不设置宽度，其宽度会自动填满父元素的宽度，可以设置宽高，即使设置了宽度，小于父元素的宽度，块级元素也会独占一行
4.  inline-block 行内块元素 与行内元素一样可以再一行内显示，而且可以设置宽高，可以设置 margin 和 padding
    示例元素：input,button,img
5.  list-item 列表元素
    示例元素：li
6.  table 会作为块级表格来显示(类似于`<table>`)，表格前后带有换行符
7.  inline-table 会作为内联表格来显示(类似于`<table>`)，表格前后没有换行符
8.  table-cell 会作为表格单元格来显示(类似于`<td>`)
9.  flex 多栏多列布局

# text-decoration 分别有哪几种值

1.  text-decoration:none //默认，定义标准的文本，没有任何样式，正常显示
2.  text-decoration:underline //定义文本下的一条线
3.  text-decoration:overline //定义文本上的一条线
4.  text-decoration:line-through //定义文本中间的一条线
5.  text-decoration:blink //定义闪烁的文本， IE.Chrome 或 Safari 不支持 "blink" 属性值
6.  text-deration:inherit //从父元素继承 text-decoration 的值，任何的版本的 IE(包括 IE8)都不支持属性值 "inherit"

# 标准盒模型和 IE 盒模型

### W3C

![w3c](img/w3cbox.jpg)

### IE

![ie](img/iebox.jpg)

# box-sizing:border-box 是什么效果

border-box 就类似于 IE 的盒模型，如果你设置了一个 width，同时设置了 box-sizing:border-box ，这时候浏览器就会帮你把 border 和 padding 计算到 width 中去

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
    <div class="content">
    </div>
</div>

.box {
    background-color: #FF8C00;
    width: 300px;
    height: 300px;
    position: relative;
}
.content {
    background-color: #F00;
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
    <div class="content">
    </div>
</div>

.box {
    background-color: #FF8C00;
    width: 300px;
    height: 300px;
    position: relative;
}
.content {
    background-color: #F00;
    width: 100px;
    height: 100px;
    position: absolute;
    left: 50%;
    top: 50%;
    transform: translate(-50%,-50%);
}
```

方案 3：flex 布局

```
<div class="box">
    <div class="content">
    </div>
</div>

.box {
    background-color: #FF8C00;
    width: 300px;
    height: 300px;
    display: flex;//flex布局
    justify-content: center;//使子项目水平居中
    align-items: center;//使子项目垂直居中
}
.content {
    background-color: #F00;
    width: 100px;
    height: 100px;
}
```

方案 4：table-cell 布局
因为 table-cell 相当与表格的 td，td 为行内元素，无法设置宽和高，所以嵌套一层，嵌套一层必须设置 display: inline-block;td 的背景覆盖了橘黄色，不推荐使用

```
<div class="box">
    <div class="content">
        <div class="inner">
        </div>
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

# 常见的浏览器兼容性问题有哪些

> 第一类：块状元素 float 后，有添加了横向的 margin，在 IE6 下比设置的值要大（属于双倍浮动的 bug）

解决方案：给 float 标签添加 display：inline，将其转换为行内元素

> 第二类：表单元素行高不一致

解决方案：给表单元素添加 float：left（左浮动）；或者是 vertical-align：middle；（垂直对齐方式：居中）

> 第三类：设置较小高度的容器（小于 10px），在 IE6 下不识别小于 10px 的高度；

解决方案：给容器添加 overflow：hidden；

> 第四类：当在 a 标签中嵌套 img 标签时，在某些浏览器中 img 会有蓝色边框；

解决方案：给 img 添加 border：0；或者是 border：none；

> 第五类：min-height 在 IE6 下不兼容

解决方案：

```
1）
min-height：value；
_height：value；
```

```
2）
min-height：value；
height：auto！important；
height：value；
```

> 第六类：图片默认有间隙

解决方案：

1）给 img 标签添加左浮动 float：left；

2）给 img 标签添加 display：block；

> 第七类：按钮默认大小不一

解决方案：

1）用 a 标签来模拟按钮，添加样式；

2）如果按钮是一张背景图片，那么直接给按钮添加背景图；

> 第八类：百分比的 bug

解决方案：父元素宽度为 100%，子元素宽度各为 50%，在 IE6 下各个元素宽度之和超过 100%

解决方案：给右边浮动的子元素添加 clear：right；

> 第九类：鼠标指针 bug

描述：cursor：hand；只有 ie 浏览器识别，其他浏览器不识别

解决方案：cursor：pointer；IE6 以上浏览器及其他内核浏览器都识别；

> 第十类：透明度属性

解决方案：针对 IE 浏览器：filter：alpha（opacity=value）；（取值范围 1--100）

兼容其他浏览器：opacity：value；（取值范围 0--1）

> 第十一类：上下 margin 的重叠问题

描述：给上边元素设置了 margin-bottom，给下边元素设置了 margin-top，浏览器只会识别较大值；

解决方案：margin-top 和 margin-bottom 中选择一个，只设置其中一个值

# 负边距

todo

# CSS Hack 有哪些

```
/* CSS属性级Hack */
color:red; /* 所有浏览器可识别*/
_color:red; /* 仅IE6 识别 */
*color:red; /* IE6.IE7 识别 */
+color:red; /* IE6.IE7 识别 */
*+color:red; /* IE6.IE7 识别 */
[color:red; /* IE6.IE7 识别 */
color:red9; /* IE6.IE7.IE8.IE9 识别 */
color:red; /* IE8.IE9 识别*/
color:red9; /* 仅IE9识别 */
color:red; /* 仅IE9识别 */
color:red !important; /* IE6 不识别!important*/
```

```
/* CSS选择符级Hack */
*html #demo { color:red;} /* 仅IE6 识别 */
*+html #demo { color:red;} /* 仅IE7 识别 */
body:nth-of-type(1) #demo { color:red;} /* IE9+.FF3.5+.Chrome.Safari.Opera 可以识别 */
head:first-child+body #demo { color:red; } /* IE7+.FF.Chrome.Safari.Opera 可以识别 */
:root #demo { color:red9; } : /* 仅IE9识别 */
```

```
/* IE条件注释Hack */
\<\!--[if IE]>此处内容只有IE可见\<\![endif]-->
\<\!--[if IE 6]>此处内容只有IE6.0可见\<\![endif]-->
\<\!--[if IE 7]>此处内容只有IE7.0可见\<\![endif]-->
\<\!--[if !IE 7]>此处内容只有IE7不能识别\<\![endif]-->
\<\!--[if gt IE 6]> IE6以上版本可识别,IE6无法识别 \<\![endif]-->
\<\!--[if gte IE 7]> IE7以及IE7以上版本可识别 \<\![endif]-->
\<\!--[if lt IE 7]> 低于IE7的版本才能识别，IE7无法识别  \<\![endif]-->
\<\!--[if lte IE 7]> IE7以及IE7以下版本可识别\<\![endif]-->
\<\!--[if !IE]>此处内容只有非IE可见\<\![endif]-->
```
