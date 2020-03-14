# Request: 获取请求消息
```java
// 获取请求方式:GET/POST
String getMethod()  
// 获取虚拟目录:/shop
String getContextPath()
// 获取Servlet路径: /login
String getServletPath()
// 获取请求URI: /shop/login
String getRequestURI()
// 获取请求URL: http://localhost/shop/login
StringBuffer getRequestURL()
// 获取协议: HTTP/1.1
String getProtocol()
// 获取客户机的IP地址
String getRemoteAddr()
// 获取所有的请求头名称
Enumeration<String> getHeaderNames()
// 通过请求头的名称获取请求头的值
String getHeader(String name)

// 获取get请求参数: name=zhangsan&...
String getQueryString()
// 获取POST请求体的字符输入流
BufferedReader getReader()
// 获取POST请求体的字节输入流
ServletInputStream getInputStream()

// 获取请求参数
String getParameter(String name)
// 获取所有参数的map集合
Map<String,String[]> getParameterMap()
```

# 中文乱码问题
在获取参数前, 设置request的编码
```java
request.setCharacterEncoding("utf-8")
```

# 请求转发:服务器内部的资源跳转方式
```java
RequestDispatcher rd = getRequestDispatcher(String path)
rd.forward(ServletRequest request, ServletResponse response) 
```
1. 浏览器地址栏路径不发生变化
2. 只能转发到当前服务器内部资源中。
3. 转发是一次请求
