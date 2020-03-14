# 快速入门
定义一个类, 实现Servlet接口
```java
public class ServletDemo1 implements Servlet {
    @Override
    public void init(ServletConfig servletConfig) throws ServletException {
        System.out.println("初始化servlet");
    }

    @Override
    public void service(ServletRequest servletRequest, ServletResponse servletResponse) throws ServletException, IOException {
        System.out.println("处理请求");
    }

    @Override
    public void destroy() {
        System.out.println("正在销毁");
    }
}
```
在web.xml中配置
```xml
<!--配置Servlet -->
<servlet>
  <servlet-name>demo1</servlet-name>
  <servlet-class>com.test.ServletDemo1</servlet-class>
</servlet>
<servlet-mapping>
  <servlet-name>demo1</servlet-name>
  <url-pattern>/demo1</url-pattern>
</servlet-mapping>
```

# 执行原理
1. 当服务器接受到客户端浏览器的请求后, 会解析请求URL路径, 获取访问的Servlet的资源路径
2. 查找web.xml文件, 是否有对应的url-pattern标签体内容。
3. 如果有, 则在找到对应的servlet-class全类名
4. tomcat会将字节码文件加载进内存, 并且创建其对象
5. 调用其方法

# Servlet3
不需要web.xml, 在类上使用@WebServlet注解, 进行配置
