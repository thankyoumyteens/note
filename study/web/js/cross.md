- <a href="#ajax如何跨域">ajax如何跨域</a>
- <a href="#ajax跨域携带cookie">ajax跨域携带cookie</a>

<a id="ajax如何跨域"></a>
# ajax如何跨域

## JSONP

```
// 创建script标签,并追加到dom中
function addScriptTag(src) {
  var script = document.createElement('script');
  script.setAttribute("type","text/javascript");
  script.src = src;
  document.body.appendChild(script);
}

// callback是接收数据并处理的函数
window.onload = function () {
  addScriptTag('http://example.com/ip?callback=foo');
}

// 服务器返回的数据: foo({"test": "testData"});
// 因为创建了script标签, 浏览器接收到数据后会立即执行(作为js脚本)
// 就会执行callback指定的函数并把数据传入
function foo(data) {
  console.log('response data: ' + JSON.stringify(data));
};
```

优点

1.  不受到同源策略的限制
2.  兼容性好，在更加古老的浏览器中都可以运行

缺点

1.  只支持 GET 请求
2.  它只支持跨域 HTTP 请求这种情况，不能解决不同域的两个页面之间如何进行 JavaScript 调用的问题。
3.  jsonp 在调用失败的时候不会返回各种 HTTP 状态码。
4.  安全性 假如它返回的 javascript 的内容被人控制的

## CORS(跨域资源共享 Cross-origin resource sharing)

服务器端:

```
// 允许的域名
response.setHeader("Access-Control-Allow-Origin", originHeader);
// 允许的请求类型，多个用逗号隔开
response.setHeader("Access-Control-Allow-Methods", "POST, GET, PUT, OPTIONS, DELETE");
// 在实际请求中，允许的自定义header，多个用逗号隔开
response.setHeader("Access-Control-Allow-Headers", "x-requested-with, Content-Type");
// 是否允许带凭证的请求(跨域cookie)
response.setHeader("Access-Control-Allow-Credentials", "true");
```

优点

1.  CORS 支持所有类型的 HTTP 请求，功能完善
2.  CORS 可以通过 onerror 事件监听错误，并且浏览器控制台会看到报错信息，利于排查。

缺点

1.  兼容性, 只支持现代浏览器
2.  对于复杂请求，CORS 会发两次请求

## 代理请求

服务器 A 的 test01.html 页面想访问服务器 B 的后台 action，
返回“test”字符串，
此时就出现跨域请求，浏览器控制台会出现报错提示，
由于跨域是浏览器的同源策略造成的，对于服务器后台不存在该问题，
可以在服务器 A 中添加一个代理 action，
在该 action 中完成对服务器 B 中 action 数据的请求，
然后在返回到 test01.html 页面

<a id="ajax跨域携带cookie"></a>
# ajax跨域携带cookie

```
var xhr = new XMLHttpRequest();  
xhr.open("POST", "http://xxxx.com/xxx", true);  
xhr.withCredentials = true; //支持跨域发送cookies
xhr.send();
```
