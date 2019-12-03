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
    // 如果是TRUE, JavaScript函数将继续执行, 而不等待服务器响应。
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
