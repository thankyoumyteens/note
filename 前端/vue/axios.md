# axios设置跨域传递cookie

## 通常我们后端这样设置跨域头
服务端将响应头设置成Access-Control-Allow-Origin：域名

## 有时, 前端需要向后端发送cookie来进行身份验证
此时, 服务器还需向响应头设置Access-Control-Allow-Credentials:true, 表示跨域时, 允许cookie添加到请求中。
另外设置Access-Control-Allow-Credentials:true后, 要将Access-Control-Allow-Origin指定到具体的域, 否则cookie不会带到客户端。

## 在express中如何设置
```
npm install cors
var cors = require('cors')
app.use(cors({credentials: true, origin: 'http://localhost:3002'}));
```
## 在ajax中的做法
XMLHttpRequest的withCredentials标志设置为true, 从而使得Cookies可以随着请求发送。因为这是一个简单的GET请求, 所以浏览器不会发送一个“预请求”。但是, 如果服务器端的响应中, 如果没有返回Access-Control-Allow-Credentials: true的响应头, 那么浏览器将不会把响应结果传递给发出请求的脚步程序, 以保证信息的安全

## 在axios中这样设置
```
axios.defaults.withCredentials = true
```
