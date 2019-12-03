# SpringMVC

## 引入依赖

```
<dependency>
  <groupId>org.springframework</groupId>
  <artifactId>spring-context</artifactId>
</dependency>

<dependency>
  <groupId>org.springframework</groupId>
  <artifactId>spring-web</artifactId>
</dependency>

<dependency>
  <groupId>org.springframework</groupId>
  <artifactId>spring-webmvc</artifactId>
</dependency>

<dependency>
  <groupId>javax.servlet</groupId>
  <artifactId>servlet-api</artifactId>
  <version>2.5</version>
  <scope>provided</scope>
</dependency>

<dependency>
  <groupId>javax.servlet.jsp</groupId>
  <artifactId>jsp-api</artifactId>
  <version>2.0</version>
  <scope>provided</scope>
</dependency>
```

## 创建spring mvc配置文件

```
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
    xmlns:mvc="http://www.springframework.org/schema/mvc"
    xmlns:context="http://www.springframework.org/schema/context"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://www.springframework.org/schema/beans 
    http://www.springframework.org/schema/beans/spring-beans.xsd
    http://www.springframework.org/schema/mvc
    http://www.springframework.org/schema/mvc/spring-mvc.xsd
    http://www.springframework.org/schema/context 
    http://www.springframework.org/schema/context/spring-context.xsd">
    
    <!-- 配置创建 spring 容器要扫描的包 -->
    <context:component-scan base-package="com.test"></context:component-scan>
    
    <!-- 配置视图解析器 -->
    <bean class="org.springframework.web.servlet.view.InternalResourceViewResolver">
        <property name="prefix" value="/WEB-INF/pages/"></property>
        <property name="suffix" value=".jsp"></property>
    </bean>
    <!-- 开启SpringMVC框架注解的支持 -->
     <mvc:annotation-driven />
</beans>
```

## 编写web.xml

```
<?xml version="1.0" encoding="UTF-8"?>
<web-app xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xmlns="http://java.sun.com/xml/ns/javaee"
    xsi:schemaLocation="http://java.sun.com/xml/ns/javaee 
    http://java.sun.com/xml/ns/javaee/web-app_2_5.xsd"
    id="WebApp_ID" version="2.5">
    
    <!-- 配置 spring mvc 的核心控制器 -->
    <servlet>
        <servlet-name>SpringMVCDispatcherServlet</servlet-name>
        <servlet-class>
            org.springframework.web.servlet.DispatcherServlet
        </servlet-class>
        <!-- 配置初始化参数, 用于读取 SpringMVC 的配置文件 -->
        <init-param>
            <param-name>contextConfigLocation</param-name>
            <param-value>classpath:SpringMVC.xml</param-value>
        </init-param>
        <!-- 配置 servlet 的对象的创建时间点：应用加载时创建。
        取值只能是非 0 正整数, 表示启动顺序 -->
        <load-on-startup>1</load-on-startup>
    </servlet>
    <servlet-mapping>
        <servlet-name>SpringMVCDispatcherServlet</servlet-name>
        <url-pattern>/</url-pattern>
    </servlet-mapping>
</web-app>
```

## 编写Controller

* `@RequestMapping`属性:
    * value：用于指定请求的 URL。它和 path 属性的作用是一样的
    * method：用于指定请求的方式(get/post/...)
    * params：用于指定限制请求参数的条件。它支持简单的表达式。要求请求参数的 key 和 value 必须和配置的一模一样

```
@Controller("helloController")
public class HelloController {

    @RequestMapping("/hello")
    public String sayHello() {
        return "success";
    }
}
```

# 请求参数绑定

## 基本类型和 String 类型作为参数

前端
```
<a href="account/findAccount?accountId=10&accountName=zhangsan">查询账户</a>
```
Controller
```
@RequestMapping("/findAccount")
public String findAccount(Integer accountId,String accountName) {
    System.out.println("查询了账户。。。。"+accountId+","+accountName);
    return "success";
}
```

## POJO 类型作为参数

实体类
```
public class Account implements Serializable {
    private Integer id;
    private String name;
    private Float money;
    private Address address;
    //getters and setters
}
```
前端
```
<form action="account/saveAccount" method="post">
    账户名称：<input type="text" name="name" ><br/>
    账户金额：<input type="text" name="money" ><br/>
    账户省份：<input type="text" name="address.provinceName" ><br/>
    账户城市：<input type="text" name="address.cityName" ><br/>
    <input type="submit" value="保存">
</form>
```
Controller
```
@RequestMapping("/saveAccount")
public String saveAccount(Account account) {
    System.out.println("保存了账户。。。。"+account);
    return "success";
}
```

# 请求参数乱码问题

在 web.xml 中配置一个过滤器
```
<!-- 配置 springMVC 编码过滤器 --> 
<filter> 
    <filter-name>CharacterEncodingFilter</filter-name> 
    <filter-class>
        org.springframework.web.filter.CharacterEncodingFilter
    </filter-class> 
    <!-- 设置过滤器中的属性值 --> 
    <init-param> 
        <param-name>encoding</param-name> 
        <param-value>UTF-8</param-value> 
    </init-param> 
</filter> 
<!-- 过滤所有请求 --> 
<filter-mapping> 
    <filter-name>CharacterEncodingFilter</filter-name> 
    <url-pattern>/*</url-pattern> 
</filter-mapping>
```

# 配置静态资源

DispatcherServlet会拦截到所有的资源, 导致一个问题就是静态资源（img、css、js）也会被拦截到, 从而
不能被使用。解决问题就是需要配置静态资源不进行拦截, 在springmvc.xml配置文件添加如下配置

1. location元素表示webapp目录下的包下的所有文件
2. mapping元素表示以/static开头的所有请求路径, 如/static/a 或者/static/a/b
```
<!-- **表示该目录下的文件以及子目录的文件 -->
<mvc:resources location="/css/" mapping="/css/**"/>
<mvc:resources location="/images/" mapping="/images/**"/>
<mvc:resources location="/scripts/" mapping="/javascript/**"/>
```

# 自定义类型转换器

* 定义一个类, 实现 Converter 接口
```
public class StringToDateConverter implements Converter<String, Date> {
    /**
    * 用于把 String 类型转成日期类型
    */
    @Override
    public Date convert(String source) {
        DateFormat format = null;
        try {
            if(StringUtils.isEmpty(source)) {
                throw new NullPointerException("请输入要转换的日期");
            }
            format = new SimpleDateFormat("yyyy-MM-dd");
            Date date = format.parse(source);
            return date;
        } catch (Exception e) {
            throw new RuntimeException("输入日期有误");
        }
    }
}
```
* 在 spring 配置文件中配置类型转换器
```
<!-- 配置类型转换器工厂 -->
<bean id="converterService"
    class="org.springframework.context.support.ConversionServiceFactoryBean">
    <!-- 给工厂注入一个新的类型转换器 -->
    <property name="converters">
        <array>
            <!-- 配置自定义类型转换器 -->
            <bean class="com.test.web.converter.StringToDateConverter"></bean>
        </array>
    </property>
</bean>

<!-- 引用自定义类型转换器 -->
<mvc:annotation-driven
    conversion-service="converterService"></mvc:annotation-driven>
```

# 使用 ServletAPI 对象作为方法参数

```
@RequestMapping("/testServletAPI")
public String testServletAPI(
    HttpServletRequest request,
    HttpServletResponse response,
    HttpSession session) {
    
    System.out.println(request);
    System.out.println(response);
    System.out.println(session);
    return "success";
}
```

# 常用注解

1. `@RequestParam`
    * 作用：把请求中指定名称的参数给控制器中的形参赋值。
    * 属性：
        * value：请求参数中的名称。
        * required：请求参数中是否必须提供此参数。默认值：true。表示必须提供, 如果不提供将报错
        
2. `@2RequestBody`
    * 作用：用于获取请求体内容。直接使用得到是 key=value&key=value...结构的数据。get 请求方式不适用。
    * 属性：
        * required：是否必须有请求体。默认值是:true。当取值为 true 时,get 请求方式会报错。如果取值为 false, get 请求得到是 null。
3. `@3PathVaribale`
    * 作用：用于绑定 url 中的占位符。例如：请求 url 中 /delete/{id}, 这个{id}就是 url 占位符。url 支持占位符是 spring3.0 之后加入的。是 springmvc 支持 rest 风格 URL 的一个重要标志。
    * 属性：
        * value：用于指定 url 中占位符名称。
        * required：是否必须提供占位符。

# ModelAndView

ModelAndView 是 SpringMVC 为我们提供的一个对象, 该对象也可以用作控制器方法的返回值。

controller
```
@RequestMapping("/testReturnModelAndView")
public ModelAndView testReturnModelAndView() {
    ModelAndView mv = new ModelAndView();
    mv.addObject("username", "张三");
    mv.setViewName("success");
    return mv;
}
```
jsp
```
<html>
<head>
    <title>执行成功</title>
</head>
<body>
    执行成功！
    ${requestScope.username}
</body>
</html>
```

# ResponseBody 响应 json 数据

添加依赖
```
<dependency>
    <groupId>com.fasterxml.jackson.core</groupId>
    <artifactId>jackson-databind</artifactId>
    <version>2.9.0</version>
</dependency>
<dependency>
    <groupId>com.fasterxml.jackson.core</groupId>
    <artifactId>jackson-core</artifactId>
    <version>2.9.0</version>
</dependency>
<dependency>
    <groupId>com.fasterxml.jackson.core</groupId>
    <artifactId>jackson-annotations</artifactId>
    <version>2.9.0</version>
</dependency>
```
发送ajax请求
```
$.ajax({
    type:"post",
    url:"/testResponseJson",
    contentType:"application/json;charset=utf-8",
    data:'{"id":1,"name":"test","money":999.0}',
    dataType:"json",
    success:function(data){
        alert(data);
    }
});
```
使用@ResponseBody 注解实现将 controller 方法返回对象转换为 json 响应给客户端
```
// spring会自动将接收的json封装成对象
@RequestMapping("/testResponseJson")
public @ResponseBody Account testResponseJson(@RequestBody Account account) {
    System.out.println("异步请求："+account);
    return account;
}
```

# 文件上传

1. form 表单的 enctype 取值必须是：multipart/form-data(默认值是:application/x-www-form-urlencoded)enctype:是表单请求正文的类型
2. method 属性取值必须是 Post
3. 提供一个文件选择域`<input type=”file” />`
4. SpringMVC框架提供了MultipartFile对象, 该对象表示上传的文件, 要求变量名称必须和表单file标签的name属性名称相同。

配置文件解析器对象
```
<!-- 配置文件解析器对象, 要求id名称必须是multipartResolver -->
<bean id="multipartResolver"
    class="org.springframework.web.multipart.commons.CommonsMultipartResolver">
    <property name="maxUploadSize" value="10485760"/>
</bean>
```
controller
```
@RequestMapping(value="/fileupload2")
public String fileupload2(HttpServletRequest request,MultipartFile upload) throws Exception {
    // 先获取到要上传的文件目录
    String path = request.getSession().getServletContext().getRealPath("/uploads");
    // 创建File对象, 一会向该路径下上传文件
    File file = new File(path);
    // 判断路径是否存在, 如果不存在, 创建该路径
    if(!file.exists()) {
        file.mkdirs();
    }
    // 获取到上传文件的名称
    String filename = upload.getOriginalFilename();
    String uuid = UUID.randomUUID().toString().replaceAll("-", "").toUpperCase();
    // 把文件的名称唯一化
    filename = uuid+"_"+filename;
    // 上传文件
    upload.transferTo(new File(file,filename));
    return "success";
}
```

# 异常处理

自定义异常处理器(实现HandlerExceptionResolver接口)
```
public class SysExceptionResolver implements HandlerExceptionResolver{

    public ModelAndView resolveException(HttpServletRequest request, HttpServletResponse response, Object handler, Exception ex) {
        ex.printStackTrace();
        ModelAndView mv = new ModelAndView();
        // 存入错误的提示信息
        mv.addObject("message", e.getMessage());
        // 跳转的Jsp页面
        mv.setViewName("error");
        return mv;
    }
}
```
配置异常处理器
```
<bean id="sysExceptionResolver" class="com.test.exception.SysExceptionResolver"/>
```

# 拦截器

Spring MVC 的处理器拦截器类似于 Servlet 开发中的过滤器 Filter, 用于对处理器进行预处理和后处理。
用户可以自己定义一些拦截器来实现特定的功能。
谈到拦截器, 还要向大家提一个词——拦截器链（Interceptor Chain）。拦截器链就是将拦截器按一定的顺
序联结成一条链。在访问被拦截的方法或字段时, 拦截器链中的拦截器就会按其之前定义的顺序被调用。
说到这里, 可能大家脑海中有了一个疑问, 这不是我们之前学的过滤器吗？是的它和过滤器是有几分相似, 但是也有区别, 接下来我们就来说说他们的区别：
* 过滤器是 servlet 规范中的一部分, 任何 java web 工程都可以使用。
* 拦截器是 SpringMVC 框架自己的, 只有使用了 SpringMVC 框架的工程才能用。
* 过滤器在 url-pattern 中配置了/*之后, 可以对所有要访问的资源拦截。
* 拦截器它是只会拦截访问的控制器方法, 如果访问的是 jsp, html,css,image 或者 js 是不会进行拦截的。

它也是 AOP 思想的具体应用。
我们要想自定义拦截器,  要求必须实现：HandlerInterceptor 接口。

HandlerInterceptor接口中的方法： 
1. preHandle方法是controller方法执行前拦截的方法
    1. 可以使用request或者response跳转到指定的页面
    2. return true放行, 执行下一个拦截器, 如果没有拦截器, 执行controller中的方法。
    3. return false不放行, 不会执行controller中的方法。
2. postHandle是controller方法执行后执行的方法, 在JSP视图执行前。
    1. 可以使用request或者response跳转到指定的页面
    2. 如果指定了跳转的页面, 那么controller方法跳转的页面将不会显示。
3. afterCompletion方法是在JSP执行后执行
    1. request或者response不能再跳转页面了

# 自定义拦截器的步骤

* 编写一个普通类实现 HandlerInterceptor 接口
```
public class HandlerInterceptorDemo1 implements HandlerInterceptor {
    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {
        System.out.println("preHandle 拦截器拦截了");
        return true;
    }
    @Override
    public void postHandle(HttpServletRequest request, HttpServletResponse response, Object handler, ModelAndView modelAndView) throws Exception {
        System.out.println("postHandle 方法执行了");
    }
    @Override
    public void afterCompletion(HttpServletRequest request, HttpServletResponse response, Object handler, Exception ex) throws Exception {
        System.out.println("afterCompletion 方法执行了");
    }
}
```
* 配置拦截器
```
<mvc:interceptors>
    <mvc:interceptor>
        <mvc:mapping path="/**"/>
        <bean id="handlerInterceptorDemo1" class="com.test.web.interceptor.HandlerInterceptorDemo1"></bean>
    </mvc:interceptor>
</mvc:interceptors>
```
