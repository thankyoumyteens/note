# 引入spring依赖
```xml
<dependency>
  <groupId>org.springframework</groupId>
  <artifactId>spring-context</artifactId>
  <version>5.0.2.RELEASE</version>
</dependency>
```

# 在类的根路径下创建 applicationContext.xml 文件
bean 标签用于让 spring 创建对象, 并且存入 ioc 容器(Map结构)之中
```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://www.springframework.org/schema/beans 
    http://www.springframework.org/schema/beans/spring-beans.xsd">
  <!-- 配置 service --> 
  <bean id="accountService" class="com.test.service.impl.AccountServiceImpl"/>
  <!-- 配置 dao -->
  <bean id="accountDao" class="com.test.dao.impl.AccountDaoImpl"/>
</beans>
```

# 加载配置
```java
// 从类的根路径下加载配置文件
ApplicationContext ac = new ClassPathXmlApplicationContext("bean.xml");
// 根据 bean 的 id 获取对象
IAccountService aService = (IAccountService) ac.getBean("accountService");
IAccountDao aDao = ac.getBean("accountDao", IAccountDao.class);
```
