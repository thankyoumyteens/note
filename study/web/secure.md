# 跨站脚本 XSS(Cross Site Scripting)

代码注入, 攻击者将恶意脚本上传执行

防范

1. 对特殊字符进行转义, 对输入数据进行验证,(是否是合法字符, 长度是否合法, 格式是否正确)

2. 设置 http-only, 避免JS读取cookie

# 跨站请求伪造 CRSF(Cross Site Request Forgery)

伪造跨站请求, 以用户的名义伪造请求发送给被攻击站点

防范

1.  在 HTTP 头中自定义属性并验证

2.  cookie 中加入 hash 随机数.

3.  检查http header: Origin Header和Referer Header
