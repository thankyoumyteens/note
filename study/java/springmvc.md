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
    <context:component-scan base-package="com.itheima"></context:component-scan>
    
    <!-- 配置视图解析器 -->
    <bean class="org.springframework.web.servlet.view.InternalResourceViewResolver">
        <property name="prefix" value="/WEB-INF/pages/"></property>
        <property name="suffix" value=".jsp"></property>
    </bean>
    <!-- 开启SpringMVC框架注解的支持 -->
     <mvc:annotation-driven conversion-service="conversionService"/>
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
        <!-- 配置初始化参数，用于读取 SpringMVC 的配置文件 -->
        <init-param>
            <param-name>contextConfigLocation</param-name>
            <param-value>classpath:SpringMVC.xml</param-value>
        </init-param>
        <!-- 配置 servlet 的对象的创建时间点：应用加载时创建。
        取值只能是非 0 正整数，表示启动顺序 -->
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
    * method：用于指定请求的方式
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

```
<!-- location 表示路径，mapping 表示文件，**表示该目录下的文件以及子目录的文件 -->
<mvc:resources location="/css/" mapping="/css/**"/>
<mvc:resources location="/images/" mapping="/images/**"/>
<mvc:resources location="/scripts/" mapping="/javascript/**"/>
```

# 自定义类型转换器

1. 定义一个类，实现 Converter 接口
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
2. 在 spring 配置文件中配置类型转换器
    ```
    <!-- 配置类型转换器工厂 -->
    <bean id="converterService"
        class="org.springframework.context.support.ConversionServiceFactoryBean">
        <!-- 给工厂注入一个新的类型转换器 -->
        <property name="converters">
            <array>
                <!-- 配置自定义类型转换器 -->
                <bean class="com.itheima.web.converter.StringToDateConverter"></bean>
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
