# Spring整体架构

![](../img/spring-overview.png)

## Core Container

Core Container（核心容器）包含Core、Beans、Context和Expression Language模块。Core和Beans模块是框架的基础部分，提供控制反转(Inversion of Control，IoC)和依赖注入(Dependency Injection，DI)特性。

- Core模块主要包含Spring框架基本的核心工具类，是其他组件的基本核心 
- Beans模块包含访问配置文件、创建和管理bean以及进行IoC/DI操作相关的所有类
- Context模块构建于Core和Beans模块基础之上，提供了一种类似于JNDI注册器的框架式的对象访问方法，ApplicationContext接口是Context模块的关键
- SpEL(Spring Expression Language)模块提供了一个表达式语言，用于在运行时查询和操纵对象

JNDI（Java Naming and Directory Interface）是Java的一个应用程序设计的API，它提供了查找和访问各种命名和目录服务的通用、统一的接口，类似于在一个中心注册一个东西，以后要用的时候，只需要根据名字去注册中心查找，注册中心返回你要的东西。

## Data Access/Integration

Data Access/Integration含JDBC、ORM、OXM、JMS和Transactions模块。

- JDBC模块提供了一个JDBC抽象层，它可以消除冗长的JDBC编码和解析数据库厂商特有的错误代码。这个模块包含了Spring对JDBC数据访问进行封装的所有类
- ORM模块为流行的对象-关系映射API(如JPA、JDO、Hibernate、iBatis等)提供了一个交互层。利用ORM封装包，可以混合使用所有Spring提供的特性进行O/R映射
- OXM模块提供了一个对Object/XML映射实现的抽象层，Object/XML映射实现包括JAXB、Castor、XMLBeans、JiBX和XStream
- JMS(Java Messaging Service)模块主要包含了一些制造和消费消息的特性
- Transactions模块支持编程和声明性的事务管理，这些事务类必须实现特定的接口，并且对所有的POJO都适用

## Web

Web上下文模块建立在应用程序上下文模块之上，为基于Web的应用程序提供了上下文。Web模块还简化了处理大部分请求以及将请求参数绑定到域对象的工作。

- Web模块提供了基础的面向Web的集成特性。例如，多文件上传、使用servlet listeners初始化IoC容器以及一个面向Web的应用上下文
- Servlet模块包含Spring的model-view-controller(MVC)实现。Spring的MVC框架使得模型范围内的代码和web forms之间能够清楚地分离开来，并与Spring框架的其他特性集成在一起
- Portlet模块：提供了用于Portlet环境和Servlet模块的MVC的实现

## AOP

AOP模块提供了一个符合AO 联盟标准的面向切面编程的实现，它让你可以定义例如方法拦截器和切点，从而将逻辑代码分开，降低它们之间的耦合性。通过配置管理特性，Spring AOP模块直接将面向切面的编程功能集成到了Spring框架中，所以可以很容易地使Spring框架管理的任何对象支持AOP。Spring AOP模块为基于Spring的应用程序中的对象提供了事务管理服务。通过使用Spring AOP，不用依赖EJB组件，就可以将声明性事务管理集成到应用程序中。

## Aspects

Aspects模块提供了对AspectJ的集成支持。AspectJ是AOP的Java语言的实现。

## Instrumentation

Instrumentation模块提供了class instrumentation支持和classloader实现，使得可以在特定的应用服务器上使用。

## Test

Test模块支持使用JUnit和TestNG对Spring组件进行测试。
