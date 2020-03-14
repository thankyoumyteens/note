# 快速入门
定义一个类, 实现Filter接口
```java
public class FilterDemo1 implements Filter {
  @Override
  public void init(FilterConfig filterConfig) throws ServletException {
  }

  @Override
  public void doFilter(ServletRequest servletRequest, ServletResponse servletResponse, FilterChain filterChain) throws IOException, ServletException {
    // ...
    // 放行
    filterChain.doFilter(servletRequest,servletResponse);
    // ...
  }

  @Override
  public void destroy() {
  }
}
```
web.xml配置
```xml
<filter>
  <filter-name>demo1</filter-name>
  <filter-class>com.test.FilterDemo1</filter-class>
</filter>
<filter-mapping>
  <filter-name>demo1</filter-name>
  <!-- 拦截路径 -->
  <url-pattern>/*</url-pattern>
</filter-mapping>
```

# 过滤器执行流程
1. 执行过滤器
2. 执行放行后的资源
3. 回来执行过滤器放行代码下边的代码

# 拦截路径配置:
1. 具体资源路径: /index.jsp   只有访问index.jsp资源时, 过滤器才会被执行
2. 拦截目录: /user/*	访问/user下的所有资源时, 过滤器都会被执行
3. 后缀名拦截: *.jsp		访问所有后缀名为jsp资源时, 过滤器都会被执行
4. 拦截所有资源:/*		访问所有资源时, 过滤器都会被执行
