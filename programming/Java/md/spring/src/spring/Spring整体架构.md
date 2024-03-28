# Spring 整体架构

![](../img/spring-overview.png)

## Core Container

Core Container(核心容器)包含 Core、Beans、Context 和 Expression Language 模块。Core 和 Beans 模块是框架的基础部分, 提供控制反转(Inversion of Control, IoC)和依赖注入(Dependency Injection, DI)特性。

- Core 模块主要包含 Spring 框架基本的核心工具类, 是其他组件的基本核心
- Beans 模块包含访问配置文件、创建和管理 bean 以及进行 IoC/DI 操作相关的所有类
- Context 模块构建于 Core 和 Beans 模块基础之上, 提供了一种类似于 JNDI 注册器的框架式的对象访问方法, ApplicationContext 接口是 Context 模块的关键
- SpEL(Spring Expression Language)模块提供了一个表达式语言, 用于在运行时查询和操纵对象

JNDI(Java Naming and Directory Interface)是 Java 的一个应用程序设计的 API, 它提供了查找和访问各种命名和目录服务的通用、统一的接口, 类似于在一个中心注册一个东西, 以后要用的时候, 只需要根据名字去注册中心查找, 注册中心返回你要的东西。

## Data Access/Integration

Data Access/Integration 含 JDBC、ORM、OXM、JMS 和 Transactions 模块。

- JDBC 模块提供了一个 JDBC 抽象层, 它可以消除冗长的 JDBC 编码和解析数据库厂商特有的错误代码。这个模块包含了 Spring 对 JDBC 数据访问进行封装的所有类
- ORM 模块为流行的对象-关系映射 API(如 JPA、JDO、Hibernate、iBatis 等)提供了一个交互层。利用 ORM 封装包, 可以混合使用所有 Spring 提供的特性进行 O/R 映射
- OXM 模块提供了一个对 Object/XML 映射实现的抽象层, Object/XML 映射实现包括 JAXB、Castor、XMLBeans、JiBX 和 XStream
- JMS(Java Messaging Service)模块主要包含了一些制造和消费消息的特性
- Transactions 模块支持编程和声明性的事务管理, 这些事务类必须实现特定的接口, 并且对所有的 POJO 都适用

## Web

Web 上下文模块建立在应用程序上下文模块之上, 为基于 Web 的应用程序提供了上下文。Web 模块还简化了处理大部分请求以及将请求参数绑定到域对象的工作。

- Web 模块提供了基础的面向 Web 的集成特性。例如, 多文件上传、使用 servlet listeners 初始化 IoC 容器以及一个面向 Web 的应用上下文
- Servlet 模块包含 Spring 的 model-view-controller(MVC)实现。Spring 的 MVC 框架使得模型范围内的代码和 web forms 之间能够清楚地分离开来, 并与 Spring 框架的其他特性集成在一起
- Portlet 模块: 提供了用于 Portlet 环境和 Servlet 模块的 MVC 的实现

## AOP

AOP 模块提供了一个符合 AO 联盟标准的面向切面编程的实现, 它让你可以定义例如方法拦截器和切点, 从而将逻辑代码分开, 降低它们之间的耦合性。通过配置管理特性, Spring AOP 模块直接将面向切面的编程功能集成到了 Spring 框架中, 所以可以很容易地使 Spring 框架管理的任何对象支持 AOP。Spring AOP 模块为基于 Spring 的应用程序中的对象提供了事务管理服务。通过使用 Spring AOP, 不用依赖 EJB 组件, 就可以将声明性事务管理集成到应用程序中。

## Aspects

Aspects 模块提供了对 AspectJ 的集成支持。AspectJ 是 AOP 的 Java 语言的实现。

## Instrumentation

Instrumentation 模块提供了 class instrumentation 支持和 classloader 实现, 使得可以在特定的应用服务器上使用。

## Test

Test 模块支持使用 JUnit 和 TestNG 对 Spring 组件进行测试。
