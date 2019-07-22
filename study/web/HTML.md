- <a href="#HTML5新特性">HTML5新特性</a>
- <a href="#语义化">语义化</a>
- <a href="#localStorage和sessionStorage">localStorage和sessionStorage</a>
- <a href="#localStorage和sessionStorage的API">localStorage和sessionStorage的API</a>
- <a href="#cookie和localStorage的区别">cookie和localStorage的区别</a>

<a id="HTML5新特性"></a>
# HTML5新特性

语义化方面: header footer nav section article section hgroup aside

视频和音频: audio video

图像方面: canvas, WebGL, SVG

数据存储: sessionStorage, localStorage

<a id="语义化"></a>
# 语义化

1. 用正确的标签做正确的事。
2. 让页面内容结构化，便于浏览器、搜索引擎解析。
3. 在去掉或丢失样式的时候能让页面呈现出清晰的结构。
4. 搜索引擎的爬虫依赖于标记来确定上下文和各个关键字的权重，有利于SEO。
5. 便于团队开发和维护，语义化更具可读性，可以减少差异性。

<a id="localStorage和sessionStorage"></a>
# localStorage和sessionStorage

- sessionStorage 存储一个会话中的数据，会话结束后数据就会被销毁

- localStorage 的数据是永久存储在客户端的，除非主动删除，否则不会过期

- 过期时间：localStorage 永久存储，永不失效除非手动删除 

- sessionStorage 浏览器重新打开后就消失了

- 大小：每个域名是 5M

<a id="localStorage和sessionStorage的API"></a>
# localStorage和sessionStorage的API

localStorage 和 sessionStorage 的 API 都是一样的，这里以 sessionStorage 为示例

```
sessionStorage.key(0) //0位索引，返回第0位数据的键值
sessionStorage.getItem("key") //键值为key的属性值
sessionStorage.setItem("key","value") //存储名为key，值为value
sessionStorage.removeItem("key") //删除键值为key的属性
sessionStorage.clear(); //删除所有sessionStorage中的属性
```

<a id="cookie和localStorage的区别"></a>
# cookie和localStorage的区别

1.  cookie 在浏览器与服务器之间来回传递 sessionStorage 和 localStorage 不会把数据发给服务器，仅在本地保存
2.  cookie 只在设置的 cookie 过期时间之前一直有效，即使窗口或浏览器关闭。
    sessionStorage 仅在当前浏览器窗口关闭前有效 localStorage 始终有效，长期保存
3.  cookie 数据不能超过 4k，sessionStorage 和 localStorage 虽然也有存储大小的限制，但比 cookie 大得多，可以达到 5M 或更大
4.  作用域不同: sessionStorage 不在不同的浏览器窗口中共享；localStorage 在所有同源窗口中都是共享的；cookie 也是在所有同源窗口中都是共享的；
