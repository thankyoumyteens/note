# Response对象: 设置响应消息
设置响应头
```java
// 设置状态码
void setStatus(int sc) 
// 设置响应头
void setHeader(String name, String value)
```
设置响应体
```java
//设置编码
response.setContentType("text/html;charset=utf-8");
// 字符输出流
PrintWriter pw = response.getWriter();
pw.write("ok");
// 字节输出流
ServletOutputStream getOutputStream();
```
# 重定向
```java
response.sendRedirect(url);
```
1. 地址栏发生变化
2. 重定向可以访问其他站点(服务器)的资源
3. 重定向是两次请求。不能使用request对象来共享数据
