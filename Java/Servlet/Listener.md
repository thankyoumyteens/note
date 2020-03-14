# Listener
将监听器绑定在事件上。 当事件发生后, 执行监听器代码
```xml
<!-- 加载spring配置文件 -->
<listener>
  <listener-class>org.springframework.web.context.ContextLoaderListener</listener-class>
</listener>
<!-- 初始化参数 -->
<context-param>
  <param-name>contextConfigLocation</param-name>
  <param-value>
      classpath:applicationContext.xml
  </param-value>
</context-param>
```
