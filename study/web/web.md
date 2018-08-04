* <a href="HTML.md">HTML</a>

* <a href="CSS.md">CSS</a>

* <a href="JavaScript.md">JavaScript</a>

* <a href="Vue.js.md">Vue.js</a>

* <a href="http.md">HTTP</a>

* <a href="browser.md">浏览器</a>

* <a href="regExp.md">正则表达式</a>

# 其他

# SEO(Search English Optimization, 搜索引擎优化)

为了使网站在搜索结果中排在前面, 更容易被用户看到

1. 首页链接不要太多(100个以内), 链接跳转次数不要太多(3次以内)
2. img标签要加上alt和title属性
3. \<meta name="keywords" content="关键词1，关键词2" />
4. \<meta name="description" content="描述1，描述2" />
5. 标签语义化
6. 少使用iframe框架

# Web 安全问题和防范

### 跨站脚本 XSS(Cross Site Scripting)

代码注入, 攻击者将恶意脚本上传执行

防范

1. 对特殊字符进行转义, 对输入数据进行验证,(是否是合法字符, 长度是否合法, 格式是否正确)

2. 设置 http-only, 避免JS读取cookie

### 跨站请求伪造 CRSF(Cross Site Request Forgery)

伪造跨站请求, 以用户的名义伪造请求发送给被攻击站点

防范

1.  在 HTTP 头中自定义属性并验证

2.  cookie 中加入 hash 随机数.

3.  检查http header: Origin Header和Referer Header

# JSON 是什么

轻量级的数据交换格式, 使用 js 语法的 **文本**

# 前端性能优化 怎么增加页面的加载速度

1. CSS Sprites(CSS精灵) 将一个页面涉及到的所有零星图片都包含到一张大图中去

2. 使用 CDN

3. 减少对DOM的操作

4. 压缩CSS和JS

5. 避免重定向
