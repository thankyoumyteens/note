- <a href="js/type.md">JavaScript数据类型</a>
- <a href="js/jsclass.md">类</a>
- <a href="#闭包">闭包</a>
- <a href="#闭包的缺点">闭包的缺点</a>
- <a href="js/event.md">事件</a>
- <a href="js/cross.md">跨域</a>
- <a href="#判断true或false">判断true或false</a>
- <a href="#设置和删除cookie">设置和删除cookie</a>
- <a href="#javascript中的this">javascript中的this</a>
- <a href="#prototype和">prototype和proto</a>
- <a href="js/scope.md">作用域.作用域链</a>
- <a href="#全文单词首字母大写">全文单词首字母大写</a>
- <a href="#ajax的工作原理和过程">ajax的工作原理和过程</a>
- <a href="#JavaScript异步加载">JavaScript异步加载</a>
- <a href="#DOMContentLoaded">DOMContentLoaded</a>
- <a href="#数组拷贝">数组拷贝</a>
- <a href="#回调地狱">回调地狱</a>
- <a href="#readyState状态">readyState状态</a>
- <a href="#改变this的指向">改变this的指向</a>
- <a href="#parseInt">将字符串转换为整数的 parseInt 的第二个参数代表什么</a>
- <a href="js/function.md">内置函数</a>
- <a href="#new">new</a>
- <a href="js/base.md">底层原理</a>
- <a href="#变量提升">变量提升</a>
- <a href="#浏览器多个标签页之间的通信">浏览器多个标签页之间的通信</a>
- <a href="#箭头函数">箭头函数</a>
- <a href="#Promise">Promise</a>
- <a href="#原型链">原型链</a>
- <a href="js/es6.md">ES6</a>

<a id="闭包"></a>
# 闭包

闭包就是能够读取其他函数内部变量的函数

```
function f1(){
    var n=999;
    function f2(){
        alert(n); // 999
    }
}
```

上面代码中的 f2 函数，就是闭包。

<a id="闭包的缺点"></a>
# 闭包的缺点

1.  由于闭包会使得函数中的变量都被保存在内存中，内存消耗很大

2.  使用闭包时，会涉及到跨作用域访问，每次访问都会导致性能损失

<a id="判断true或false"></a>
# 判断true或false

值为 false

```
new Boolean();
Boolean(0);
Boolean(null);
Boolean(undefined);
Boolean("");
Boolean(false);
Boolean(NaN);
```

其他情况均为 true

```
Boolean({}) // true
Boolean([]) // true
Boolean("null") // true
Boolean("0") // true
```

<a id="设置和删除cookie"></a>
# 设置和删除cookie

```
// 设置cookie
// key: 键, value: 值, expires: 有效时长(ms)
function setCookie(key, value, expires) {
    let d = new Date();
    d.setTime(d.getTime() + expires);
    document.cookie = key + "=" + value + "; " + "expires="+d.toUTCString();
}

// 获取cookie
function getCookie(cname) {
    var name = cname + "=";
    var ca = document.cookie.split(';');
    for(var i=0; i<ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1);
        if (c.indexOf(name) != -1) return c.substring(name.length, c.length);
    }
    return "";
}

// 清除cookie  
function clearCookie(key) {
    setCookie(key, "", -1);  
}  
```

<a id="javascript中的this"></a>
# javascript中的this

this 永远指向的是最后调用它的对象，也就是看它执行的时候是谁调用的

<a id="prototype和"></a>
# prototype和\_\_proto\_\_

显示原型(prototype): 显示原型实现基于原型的继承和属性的共享

隐式原型(\[\[prototype\]\]): 隐式原型是的作用就是构成原型链, 
通过隐式原型可以一层层往上查找对象的原型 \_\_proto\_\_是个不标准的属性, 
是浏览器为了实现对\[\[prototype\]\]的访问所提供的一个方法, 
常理来说\[\[prototype\]\]即隐式原型是不可访问的,
ES5 里提供了 Object.getPrototypeOf()这个方法来获得\[\[prototype\]\]

prototype 和\_\_proto\_\_都指向原型对象, 
任意一个函数(包括构造函数)都有一个 prototype 属性, 
指向该函数的原型对象，同样 **任意一个构造函数实例化的对象** , 
都有一个\_\_proto\_\_属性, 指向构造函数的原型对象

```
function Foo(){}
var Boo = {name: "Boo"};
Foo.prototype = Boo;
var f = new Foo();

console.log(f.__proto__ === Foo.prototype); // true
console.log(f.__proto__ === Boo);   // true
Object.getPrototypeOf(f) === f.__proto__;   // true

let b = 1;
console.log(b.__proto__ === Number.prototype) // true
console.log(1.__proto__) // Uncaught SyntaxError: Invalid or unexpected token
```

![proto](img/proto.png)

<a id="全文单词首字母大写"></a>
# 全文单词首字母大写

```
function ReplaceFirstUper(str)  
{
    str = str.toLowerCase();
    return str.replace(/\b(\w)|\s(\w)/g, function(m){  
        return m.toUpperCase();  
    });
}

console.log(ReplaceFirstUper('i have a pen, i have an apple!'));
// 输出: I Have A Pen, I Have An Apple!
```

<a id="ajax的工作原理和过程"></a>
# ajax的工作原理和过程

Ajax 的工作原理相当于在用户和服务器之间加了—个中间层(AJAX 引擎),使用户操作与服务器响应异步化 并不是所有的用户请求都提交给服务器,像—些数据验证和数据处理等都交给 Ajax 引擎自己来做, 只有确定需要从服务器读取新数据时再由 Ajax 引擎代为向服务器提交请求

Ajax 异步请求

请求过程：浏览器(当前页面不会丢弃) --> Ajax 引擎(http 协议) --> Web 服务器

响应过程：Web 服务器 --> 准备部分数据 ---> Ajax 引擎(http 协议) --> dom 编程

Ajax 的工作过程

1.  创建 Ajax 引擎对象(XMLHttpRequest(其它).ActiveXObject(ie))

2.  打开服务器之间的连接

3.  发送异步请求

4.  获取服务器端的响应数据

```
function getData() {
    // 1. 创建Ajax引擎对象
    var xmlhttp = null;
    // 非IE浏览器创建XmlHttpRequest对象
    if (window.XmlHttpRequest) {
        xmlhttp = new XmlHttpRequest();
    }
    // IE浏览器创建XmlHttpRequest对象
    if (window.ActiveXObject) {
        try { xmlhttp = new ActiveXObject("Microsoft.XMLHTTP"); }
        catch (e) {
            try { xmlhttp = new ActiveXObject("msxml2.XMLHTTP"); }
            catch (ex) {}
        }
    }
    if (!xmlhttp) {
        alert("创建xmlhttp对象异常！");
        return false;
    }
    // 2. 打开服务器之间的连接
    // 第三个参数设置请求是否为异步模式。
    // 如果是TRUE，JavaScript函数将继续执行，而不等待服务器响应。
    // 同步：提交请求->等待服务器处理->处理完毕返回 这个期间客户端浏览器不能干任何事
    // 异步: 请求通过事件触发->服务器处理（这是浏览器仍然可以作其他事情）->处理完毕
    xmlhttp.open("POST", url, false);

    xmlhttp.onreadystatechange = function () {
        if (xmlhttp.readyState == 4) {
            document.getElementById("user1").innerHTML = "数据正在加载...";
            // 4. 获取服务器端的响应数据
            if (xmlhttp.status == 200) {
                console.log(xmlhttp.responseText);
            }
        }
    }
    // 3. 发送异步请求
    xmlhttp.send();
}
```

<a id="JavaScript异步加载"></a>
# JavaScript异步加载

## defer="defer"和 async="true/false"

async: 加载后续文档元素的过程将和 JS 的加载与执行并行进行（异步）

defer: 加载后续文档元素的过程将和 JS 的加载并行进行（异步），但 JS 的执行要在所有文档元素解析完成之后，DOMContentLoaded 事件触发之前完成

使用这两个属性的脚本中不能调用 document.write 方法

## 动态创建 script

```
function addScriptTag(src){
    var script = document.createElement('script');
    script.setAttribute("type","text/javascript");
    script.src = src;
    document.body.appendChild(script);
}
window.onload = function(){
    addScriptTag("js/index.js");
}
```

<a id="DOMContentLoaded"></a>
# DOMContentLoaded

当页面文档加载并解析完毕之后会马上触发 DOMContentLoaded 事件，
而不会等待样式文件.图片文件和子框架页面的加载

```
document.addEventListener("DOMContentLoaded", function(event) {
    console.log("DOM fully loaded and parsed");
});
```

<a id="数组拷贝"></a>
# 数组拷贝

## 数组深拷贝

1.  简单方法: `arr2 = JSON.parse(JSON.stringify(arr1));`
2.  递归

## 数组浅拷贝

1.  `arr2 = arr1.slice(0);`
2.  `arr2 = arr1.concat();`

<a id="回调地狱"></a>
# 回调地狱

```
fs.readFile('./sample.txt', 'utf-8', (err, content) => {
    let keyword = content.substring(0, 5);
    db.find(`select * from sample where kw = ${keyword}`, (err, res) => {
        get(`/sampleget?count=${res.length}`, data => {
           console.log(data);
        });
    });
});
```

每增加一个异步请求，就会多添加一层回调函数的嵌套，这段代码中三个异步函数的嵌套已经开始使一段本可以语言明确的代码编程不易阅读与维护了。

左侧明显出现了一个三角形的缩进区域，过多的回调也就让我们陷入“回调地狱”。

## Promise 解决回调地狱

嵌套操作变成了通过 then 连接的链式操作。代码的整洁度上有了一个较大的提高。

```
function getData(url) {
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            resolve(url.replace('url', 'data'))
        }, 1000)
    })
}

function doTest() {
    getData('url_111').then(data => {
        console.log(data)
        // getData('url_222').then(data => {
        //     console.log(data)
        // })
        return getData('url_222')
    }).then(data => {
        console.log(data)
        return getData('url_333')
    }).then(data => {
        console.log(data)
    })
}

doTest()
```

<a id="readyState状态"></a>
# readyState状态

- 0: 未初始化 XMLHttpRequest对象已经创建，但还没有调用 open()方法。值为 0 表示对象已经存在，否则浏览器会报错：对象不存在。
- 1: 正在发送请求 对 XMLHttpRequest 对象进行初始化，即调用 open()方法，根据参数(method,url,true)，完成对象状态的设置。并调用 send()方法开始向服务端发送请求。值为 1 表示正在向服务端发送请求。
- 2: 载入完成 此阶段接收服务器端的响应数据。但获得的还只是服务端响应的原始数据，并不能直接在客户端使用。值为 2 表示 send()方法执行完成，已经接收完全部响应数据。并为下一阶段对数据解析作好准备。
- 3: 解析数据 正在解析响应内容 此阶段解析接收到的服务器端响应数据。即根据服务器端响应头部返回的 MIME 类型把数据转换成能通过 responseBody.responseText 或 responseXML 属性存取的格式，为在客户端调用作好准备。值为 3 表示正在解析数据。
- 4: 响应内容解析完成 此阶段确认全部数据都已经解析为客户端可用的格式，解析已经完成。值为 4 表示数据解析完毕，可以通过 XMLHttpRequest 对象的相应属性取得数据。

<a id="改变this的指向"></a>
# 改变this的指向，call和apply和bind的区别

1.  call(this 指向谁,arg1,arg2,...) // 参数一个一个传

2.  apply(this 指向谁,[arg1,arg2...]) // 参数为数组

3.  bind(this 指向谁) // 定义时不传参，调用时再传参

```
var a=2;
var json = {
    a: 1,
    show(){
        // alert(this.a); // 输出：1
        setTimeout(function(){
            // setTimeout中this默认为window,
            // 使用bind()改变this为json对象
            alert(this.a);
        }.bind(this),1000)
    }
}
json.show();// 正确输出：1，而不是：2
```

<a id="parseInt"></a>
# 将字符串转换为整数的 parseInt 的第二个参数代表什么

转换成几进制

<a id="new"></a>
# new

1.  创建一个新对象；
2.  将构造函数的作用域赋给新对象（因此 this 就指向了这个新对象） ；
3.  执行构造函数中的代码（为这个新对象添加属性） ；
4.  返回新对象。

```
var obj = new Base();
```

```
var obj  = {};
obj.__proto__ = Base.prototype;
Base.call(obj);
```

<a id="变量提升"></a>
# 变量提升

JavaScript 引擎的工作方式是，先解析代码，
获取所有被声明的变量，然后再一行一行地运行。
这造成的结果，就是所有的变量的声明语句，都会被提升到代码的头部，
这就叫做变量提升。

变量提升只对 var 命令声明的变量有效，如果一个变量不是用 var 命令声明的，就不会发生变量提升

```
console.log(a); // undefined
var a =1;
console.log(aa); // ReferenceError: aa is not defined
aa =1;
```

let/const 声明的变量存在变量提升， 
但是由于死区(当前作用域顶部到该变量声明位置中间的部分，都是该 let 变量的死区)
我们无法在声明前访问这个变量

```
console.log(a);// ReferenceError: a is not defined
let a = 1;
```

<a id="浏览器多个标签页之间的通信"></a>
# 浏览器多个标签页之间的通信

页面 A 数据改变, 页面 B 也跟着改变

1.  websocket

2.  在页面 A 设置一个使用定时器不断刷新，检查 Cookies 的值是否发生变化，如果变化就进行更新

3.  监听 localstorage 事件, 当前页面修改 localStorage 会触发其他页面的监听函数

```
// 页面B设置
window.addEventListener('storage', (e) => console.log(e))
```

4.  SharedWorker

<a id="箭头函数"></a>
# 箭头函数

优势

- 更加简洁

- 修复了 this 的指向

普通函数中的 this:

1.  this 总是代表它的直接调用者(js 的 this 是执行上下文), 例如 obj.func ,那么 func 中的 this 就是 obj

2.  非严格模式下, 没找到直接调用者,则 this 指的是 window

3.  在严格模式下, 没找到直接调用者,则 this 指的是 undefined

4.  使用 call,apply,bind 可以改变 this 的指向

箭头函数中的 this

箭头函数没有自己的 this(也没有 arguments), 它的 this(和 arguments)是从父作用域继承而来; 默认指向在定义它时所处的对象(宿主对象),而不是执行时的对象

由于箭头函数不绑定 this, 它会捕获其所在上下文(即定义的位置)的 this 值, 作为自己的 this 值

所以 call() / apply() / bind() 方法对于箭头函数来说只是传入参数，对它的 this 毫无影响。

```
function P() {
    this.tmp = 0;
    setInterval(function () {
        // this -> Window
        this.tmp++;
        console.log('P -> ' + this.tmp);
    }, 1000);
}

function P2(val) {
    this.tmp2 = val;
    setInterval(() => {
        // this -> P2实例化的对象
        this.tmp2++;
        console.log('P2 -> ' + this.tmp2);
    }, 1000);
}

let o = new P();
let o2 = new P2(0);
let o3 = new P2(100);

/*
    输出:
    P -> NaN
    P2 -> 1
    P2 -> 101
    P -> NaN
    P2 -> 2
    P2 -> 102
    P -> NaN
    P2 -> 3
    P2 -> 103
*/
```

<a id="Promise"></a>
# Promise

三种状态:

1.  Pending(进行中)
2.  Fulfilled(已完成)
3.  Rejected(已失败)

Promise 对象的状态改变，只有两种可能: 从 Pending 变为 Fulfilled 和从 Pending 变为 Rejected。只要这两种情况发生，状态就不会再变了

常用方法

- Promise.all

Promise.all 可以将多个 Promise 实例包装成一个新的 Promise 实例。成功的时候返回(等到所有 Promise 完成后才返回)的是一个结果数组，失败的时候则返回最先被 reject 失败状态的值。

```
let p1 = new Promise((resolve, reject) => {
    resolve('p1')
})

let p2 = new Promise((resolve, reject) => {
    resolve('p2')
})

Promise.all([p1, p2]).then((result) => {
    console.log(result) // ['p1', 'p2']
})
```

- Promise.race

返回最先完成的结果，不管结果本身是成功状态还是失败状态。

实现原理

todo

<a id="原型链"></a>
# 原型链

todo
