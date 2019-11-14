# 使用XML配置文件实现IoC

## 引入spring依赖

```
<dependency>
    <groupId>org.springframework</groupId>
    <artifactId>spring-context</artifactId>
    <version>5.0.2.RELEASE</version>
</dependency>
```

## 在类的根路径下创建一个任意名称的 xml 文件

bean 标签：用于配置让 spring 创建对象，并且存入 ioc 容器(Map结构)之中

bean 标签的属性：
1. id：给对象在容器中提供一个唯一标识。用于获取对象。
2. class：指定类的全限定类名。用于反射创建对象。默认情况下调用无参构造函数。
3. scope：指定对象的作用范围。
    * singleton :默认值，单例的
    * prototype :多例的

```
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

## 测试配置是否成功

```
//1.使用 ApplicationContext 接口
// ClassPathXmlApplicationContext: 从类的根路径下加载配置文件
ApplicationContext ac = new ClassPathXmlApplicationContext("bean.xml");
//2.根据 bean 的 id 获取对象
IAccountService aService = (IAccountService) ac.getBean("accountService");
IAccountDao aDao = ac.getBean("accountDao", IAccountDao.class);
```

# 实例化 Bean 的三种方式

1. 使用默认无参构造函数
    ```
    <!--
        在默认情况下：
        它会根据默认无参构造函数来创建类对象。
        如果 bean 中没有默认无参构造函数，将会创建失败。
    -->
    <bean 
        id="accountService" 
        class="com.test.service.impl.AccountServiceImpl"/>
    ```
2. 使用其他类的静态方法创建对象

    bean 标签的属性:
    * id 属性：指定 bean 的 id，用于从容器中获取
    * class 属性：指定静态工厂的全限定类名
    * factory-method 属性：指定生产对象的静态方法
    ```
    <!-- 
        此种方式是:
        使用 StaticFactory 类中的
        静态方法 createAccountService 创建对象，
        并存入 spring 容器
    -->
    <bean id="accountService"
        class="com.test.factory.StaticFactory"
        factory-method="createAccountService"/>
    ```
3. 使用其他对象的方法创建对象

    bean 标签的属性:
    * factory-bean 属性：用于指定实例工厂 bean 的 id。
    * factory-method 属性：用于指定实例工厂中创建对象的方法。
    ```
    <!-- 
        此种方式是：
        先把工厂的创建交给 spring 来管理。
        然后在使用工厂的 bean 来调用里面的方法
    -->
    <bean id="instancFactory" 
        class="com.test.factory.InstanceFactory"/>
    <bean id="accountService"
        factory-bean="instancFactory"
        factory-method="createAccountService"/>
    ```

# 依赖注入(给bean注入数据)

## 能注入的数据

1. 基本类型和String
2. 其他bean类型(在配置文件或注解配置过的bean)
3. 集合类型

## 注入的方式

1. 使用构造方法注入
2. 使用setter注入
3. 使用注解注入

## 构造函数注入

```
public AccountServiceImpl(String name, Integer age, Date birthday) {
    this.name = name;
    this.age = age;
    this.birthday = birthday;
}
```
constructor-arg标签: 

属性：
* index:指定参数在构造函数参数列表的索引位置
* type:指定参数在构造函数中的数据类型name:指定参数在构造函数中的名称 用这个找给谁赋值
* value:它能赋的值是基本数据类型和 String 类型
* ref:它能赋的值是其他 bean 类型，也就是说，必须得是在配置文件中配置过的 bean
```
<bean id="accountService" class="com.test.service.impl.AccountServiceImpl">
    <constructor-arg name="name" value="张三"/>
    <constructor-arg name="age" value="18"/>
    <constructor-arg name="birthday" ref="now"/>
</bean>
<bean id="now" class="java.util.Date"></bean>
```

## setter 方法注入

```
public void setName(String name) {
    this.name = name;
}
public void setAge(Integer age) {
    this.age = age;
}
public void setBirthday(Date birthday) {
    this.birthday = birthday;
}
```
property标签: 

属性： 
* name：找的是类中 set 方法后面的部分
* ref：给属性赋值是其他 bean 类型的
* value：给属性赋值是基本数据类型和 string 类型的
```
<bean id="accountService" class="com.test.service.impl.AccountServiceImpl">
    <property name="name" value="test"/>
    <property name="age" value="21"/>
    <property name="birthday" ref="now"/>
</bean>
<bean id="now" class="java.util.Date"></bean>
```

## 注入集合

```
<bean id="accountService" class="com.test.service.impl.AccountServiceImpl">
    <!-- 在注入集合数据时，只要结构相同，标签可以互换 -->
    <!-- 给数组注入数据 -->
    <property name="myStrs">
        <set>
            <value>AAA</value>
            <value>BBB</value>
            <value>CCC</value>
        </set>
    </property>
    <!-- 注入 list 集合数据 -->
    <property name="myList">
        <array>
            <value>AAA</value>
            <value>BBB</value>
            <value>CCC</value>
        </array>
    </property>
    <!-- 注入 set 集合数据 -->
    <property name="mySet">
        <list>
            <value>AAA</value>
            <value>BBB</value>
            <value>CCC</value>
        </list>
    </property>
    <!-- 注入 Map 数据 -->
    <property name="myMap">
        <props>
            <prop key="testA">aaa</prop>
            <prop key="testB">bbb</prop>
        </props>
    </property>
    <!-- 注入 properties 数据 -->
    <property name="myProps">
    <map>
        <entry key="testA" value="aaa"></entry>
        <entry key="testB">
            <value>bbb</value>
        </entry>
    </map>
    </property>
</bean>
```

# 注解

## 定义配置文件指定使用了注解的类所在的包

```
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xmlns:context="http://www.springframework.org/schema/context"
       xsi:schemaLocation="http://www.springframework.org/schema/beans
        http://www.springframework.org/schema/beans/spring-beans.xsd
        http://www.springframework.org/schema/context
        http://www.springframework.org/schema/context/spring-context.xsd">

    <!--
        告知spring框架在，
        读取配置文件，创建容器时，
        扫描指定包下的类，
        依据类中使用的注解创建对象，并存入容器中 
    -->
    <context:component-scan base-package="com.test"/>
</beans>
```

## 用于创建对象的
他们的作用就和在XML配置文件中编写一个<bean>标签实现的功能是一样的


1. `@Component`: 
    * 作用: 用于把当前类对象存入spring容器中
    * 属性：
        * value：用于指定bean的id。当我们不写时，它的默认值是当前类名，且首字母改成小写。
* `@Controller`： 一般用在表现层
* `@Service`： 一般用在业务层
* `@Repository`： 一般用在持久层

以上三个注解他们的作用和属性与Component是一模一样。
他们三个是spring框架为我们提供明确的三层使用的注解，使我们的三层对象更加清晰

## 用于注入数据的
他们的作用就和在xml配置文件中的bean标签中写一个<property>标签的作用是一样的

1. `@Autowired`:
    * 作用：自动按照类型注入。只要容器中有唯一的一个bean对象类型和要注入的变量类型匹配，就可以注入成功
    * 属性: 无
    * 如果ioc容器中没有任何bean的类型和要注入的变量类型匹配，则报错。
    * 如果Ioc容器中有多个类型匹配时：如果存在和要注入的变量的同名的bean，则使用这个bean， 如果没有则报错
    * 出现位置： 可以是变量上，也可以是方法上
    * 细节： 在使用此注解注入时，不用写setter方法。
2. `@Qualifier`:
    * 作用：在按照类型注入的基础之上再按照名称注入。它在给类成员注入时不能单独使用。但是在给方法参数注入时可以
    * 属性：
        * value：用于指定注入bean的id。
3. `@Resource`: 
    * 作用：直接按照bean的id注入。它可以独立使用
    * 属性：
        * name：用于指定bean的id。

以上三个注入都只能注入其他bean类型的数据，而基本类型和String类型无法使用上述注解实现。

另外，集合类型的注入只能通过XML来实现。

1. `@Value`: 
    * 作用：用于注入基本类型和String类型的数据
    * 属性：
        * value：用于指定数据的值。

## 用于改变作用范围的
他们的作用就和在bean标签中使用scope属性实现的功能是一样的

1. `@Scope`: 
    * 作用：用于指定bean的作用范围
    * 属性：
        * value：指定范围的取值。常用取值：singleton和prototype

# 使用注解替换xml配置文件

1. `@Configuration`
    * 作用：指定当前类是一个配置类
    * 细节：当配置类作为AnnotationConfigApplicationContext对象创建的参数时，该注解可以不写。
2. `@ComponentScan`
    * 作用：用于通过注解指定spring在创建容器时要扫描的包
    * 属性：
        * value：它和basePackages的作用是一样的，都是用于指定创建容器时要扫描的包。
    * 我们使用此注解就等同于在xml中配置了:
        ```
        <context:component-scan base-package="com.test"/>
        ```
3. `@Bean`
    * 作用：用于把当前方法的返回值作为bean对象存入spring的ioc容器中
    * 属性:
        * name:用于指定bean的id。当不写时，默认值是当前方法的名称
    * 细节： 当我们使用注解配置方法时，如果方法有参数，spring框架会去容器中查找有没有可用的bean对象。
    查找的方式和Autowired注解的作用是一样的
4. `@Import`
    * 作用：用于导入其他的配置类
    * 属性：
        * value：用于指定其他配置类的字节码。
5. `@PropertySource`
    * 作用：用于指定properties文件的位置
    * 属性：
        * value：指定文件的名称和路径。关键字：classpath，表示类路径下
        
# Spring 整合 Junit

## 引入依赖

```
<dependency>
    <groupId>org.springframework</groupId>
    <artifactId>spring-test</artifactId>
    <version>5.0.2.RELEASE</version>
</dependency>
```

## 使用@RunWith 注解替换原有运行器

```
@RunWith(SpringJUnit4ClassRunner.class)
public class AccountServiceTest {}
```

## 使用@ContextConfiguration 指定 spring 配置文件的位置
```
@RunWith(SpringJUnit4ClassRunner.class)
@ContextConfiguration(locations= {"classpath:bean.xml"})
public class AccountServiceTest {}
```

## 使用@Autowired 注入数据
```
@RunWith(SpringJUnit4ClassRunner.class)
@ContextConfiguration(locations= {"classpath:bean.xml"})
public class AccountServiceTest {
    @Autowired
    private IAccountService as = null;

    @Test
    public void testFindAll() {
        List<Account> accounts = as.findAllAccount();
        for(Account account : accounts){
            System.out.println(account);
        }
    }
}
```

# 基于XML的AOP配置

## 引入依赖

```
<dependency>
    <groupId>org.springframework</groupId>
    <artifactId>spring-context</artifactId>
    <version>5.0.2.RELEASE</version>
</dependency>

<dependency>
    <groupId>org.aspectj</groupId>
    <artifactId>aspectjweaver</artifactId>
    <version>1.8.7</version>
</dependency>
```

## 切入点表达式的写法

* 关键字：execution(表达式)
* 表达式：访问修饰符  返回值  包名.包名.包名...类名.方法名(参数列表)
* 标准的表达式写法：`public void com.test.service.impl.AccountServiceImpl.saveAccount()`
* 访问修饰符可以省略: `void com.test.service.impl.AccountServiceImpl.saveAccount()`
* 返回值可以使用通配符，表示任意返回值: `* com.test.service.impl.AccountServiceImpl.saveAccount()`
* 包名可以使用通配符，表示任意包。但是有几级包，就需要写几个*.: `* *.*.*.*.AccountServiceImpl.saveAccount())`
* 包名可以使用..表示当前包及其子包: `* *..AccountServiceImpl.saveAccount()`
* 类名和方法名都可以使用*来实现通配: `* *..*.*()`
* 参数列表：
    * 可以直接写数据类型：
        * 基本类型直接写名称: int
        * 引用类型写包名.类名的方式: java.lang.String
    * 可以使用通配符表示任意类型，但是必须有参数
    * 可以使用..表示有无参数均可，有参数可以是任意类型
* 全通配写法：`* *..*.*(..)`
* 切到业务层实现类下的所有方法: `* com.test.service.impl.*.*(..)`

## 配置AOP, 使service的每个方法调用之前都执行Logger的printLog方法

1. 把通知Bean也交给spring来管理
2. 使用aop:config标签表明开始AOP的配置
3. 使用aop:aspect标签表明配置切面
    * id属性：是给切面提供一个唯一标识
    * ref属性：是指定通知类bean的Id。
4. 在aop:aspect标签的内部使用对应标签来配置通知的类型
    * aop:before：表示配置前置通知
        * method属性：用于指定Logger类中哪个方法是前置通知
        * pointcut属性：用于指定切入点表达式，该表达式的含义指的是对业务层中哪些方法增强
```
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
   xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
   xmlns:aop="http://www.springframework.org/schema/aop"
   xsi:schemaLocation="http://www.springframework.org/schema/beans
    http://www.springframework.org/schema/beans/spring-beans.xsd
    http://www.springframework.org/schema/aop
    http://www.springframework.org/schema/aop/spring-aop.xsd">
    <!-- 配置srping的Ioc,把service对象配置进来-->
    <bean id="accountService" class="com.test.service.impl.AccountServiceImpl"></bean>
    <!-- 配置Logger类 -->
    <bean id="logger" class="com.test.utils.Logger"></bean>
    
    <!--配置AOP-->
    <aop:config>
        <!--配置切面 -->
        <aop:aspect id="logAdvice" ref="logger">
            <!-- 配置通知的类型，并且建立通知方法和切入点方法的关联-->
            <aop:before method="printLog" pointcut="execution(* com.test.service.impl.*.*(..))"></aop:before>
        </aop:aspect>
    </aop:config>
</beans>
```

# 切面的通知类型

1. 前置通知：在切入点方法执行之前执行
2. 后置通知：在切入点方法正常执行之后执行
3. 异常通知：在切入点方法执行产生异常之后执行
4. 最终通知：无论切入点方法是否正常执行它都会在其后面执行

```
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
   xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
   xmlns:aop="http://www.springframework.org/schema/aop"
   xsi:schemaLocation="http://www.springframework.org/schema/beans
    http://www.springframework.org/schema/beans/spring-beans.xsd
    http://www.springframework.org/schema/aop
    http://www.springframework.org/schema/aop/spring-aop.xsd">

<!-- 配置srping的Ioc,把service对象配置进来-->
<bean id="accountService" class="com.test.service.impl.AccountServiceImpl"></bean>
<!-- 配置Logger类 -->
<bean id="logger" class="com.test.utils.Logger"></bean>

<!--配置AOP-->
<aop:config>
    <!-- 配置切入点表达式 id属性用于指定表达式的唯一标识。expression属性用于指定表达式内容
          此标签写在aop:aspect标签内部只能当前切面使用。
          它还可以写在aop:aspect外面，此时就变成了所有切面可用
      -->
    <aop:pointcut id="pt1" expression="execution(* com.test.service.impl.*.*(..))"></aop:pointcut>
    <!--配置切面 -->
    <aop:aspect id="logAdvice" ref="logger">
        <!-- 配置前置通知：在切入点方法执行之前执行
        <aop:before method="beforePrintLog" pointcut-ref="pt1" ></aop:before>-->
        <!-- 配置后置通知：在切入点方法正常执行之后执行。它和异常通知永远只能执行一个
        <aop:after-returning method="afterReturningPrintLog" pointcut-ref="pt1"></aop:after-returning>-->
        <!-- 配置异常通知：在切入点方法执行产生异常之后执行。它和后置通知永远只能执行一个
        <aop:after-throwing method="afterThrowingPrintLog" pointcut-ref="pt1"></aop:after-throwing>-->
        <!-- 配置最终通知：无论切入点方法是否正常执行它都会在其后面执行
        <aop:after method="afterPrintLog" pointcut-ref="pt1"></aop:after>-->
    </aop:aspect>
</aop:config>
</beans>
```

# 环绕通知

环绕通知：
* 问题：当我们配置了环绕通知之后，切入点方法没有执行，而通知方法执行了。
* 分析：通过对比动态代理中的环绕通知代码，发现动态代理的环绕通知有明确的切入点方法调用，而我们的代码中没有。
* 解决：Spring框架为我们提供了一个接口：ProceedingJoinPoint。该接口有一个方法proceed()，此方法就相当于明确调用切入点方法。
该接口可以作为环绕通知的方法参数，在程序执行时，spring框架会为我们提供该接口的实现类供我们使用。
* spring中的环绕通知：它是spring框架为我们提供的一种可以在代码中手动控制增强方法何时执行的方式。

```
<!--配置AOP-->
<aop:config>
    <aop:pointcut id="pt1" expression="execution(* com.test.service.impl.*.*(..))"></aop:pointcut>
    <!--配置切面 -->
    <aop:aspect id="logAdvice" ref="logger">
        <!-- 配置环绕通知-->
        <aop:around method="aroundPringLog" pointcut-ref="pt1"></aop:around>
    </aop:aspect>
</aop:config>
```

```
package com.test.utils;

import org.aspectj.lang.ProceedingJoinPoint;

/**
 * 用于记录日志的工具类，它里面提供了公共的代码
 */
public class Logger {
    public Object aroundPringLog(ProceedingJoinPoint pjp){
        Object rtValue = null;
        try{
            Object[] args = pjp.getArgs();//得到方法执行所需的参数

            System.out.println("Logger类中的aroundPringLog方法开始记录日志了。。。前置");

            rtValue = pjp.proceed(args);//明确调用业务层方法（切入点方法）

            System.out.println("Logger类中的aroundPringLog方法开始记录日志了。。。后置");

            return rtValue;
        }catch (Throwable t){
            System.out.println("Logger类中的aroundPringLog方法开始记录日志了。。。异常");
            throw new RuntimeException(t);
        }finally {
            System.out.println("Logger类中的aroundPringLog方法开始记录日志了。。。最终");
        }
    }
}
```

# 事务控制

1. JavaEE 体系进行分层开发，事务处理位于业务层，Spring 提供了分层设计业务层的事务处理解决方案
2. spring 框架为我们提供了一组事务控制的接口。这组接口是在spring-tx-5.0.2.RELEASE.jar 中。
3. spring 的事务控制都是基于 AOP 的，它既可以使用编程的方式实现，也可以使用配置的方式实现

事务的传播行为

* REQUIRED:如果当前没有事务，就新建一个事务，如果已经存在一个事务中，加入到这个事务中。一般的选择（默认值）
* SUPPORTS:支持当前事务，如果当前没有事务，就以非事务方式执行（没有事务）

# 基于 XML 的声明式事务控制

## 引入依赖

```
<dependency>
    <groupId>org.springframework</groupId>
    <artifactId>spring-context</artifactId>
    <version>5.0.2.RELEASE</version>
</dependency>

<dependency>
    <groupId>org.springframework</groupId>
    <artifactId>spring-tx</artifactId>
    <version>5.0.2.RELEASE</version>
</dependency>

<dependency>
    <groupId>mysql</groupId>
    <artifactId>mysql-connector-java</artifactId>
    <version>5.1.6</version>
</dependency>

<dependency>
    <groupId>org.aspectj</groupId>
    <artifactId>aspectjweaver</artifactId>
    <version>1.8.7</version>
</dependency>
```

## 编写业务层代码

```
@Override
public void transfer(String sourceName, String targetName, Float money) {
    System.out.println("transfer....");
    //2.1根据名称查询转出账户
    Account source = accountDao.findAccountByName(sourceName);
    //2.2根据名称查询转入账户
    Account target = accountDao.findAccountByName(targetName);
    //2.3转出账户减钱
    source.setMoney(source.getMoney()-money);
    //2.4转入账户加钱
    target.setMoney(target.getMoney()+money);
    //2.5更新转出账户
    accountDao.updateAccount(source);
    //2.6更新转入账户
    accountDao.updateAccount(target);
}
```

## 配置文件

### spring中基于XML的声明式事务控制配置步骤
1. 配置事务管理器
2. 配置事务的通知tx:advice
    * 属性：
        * id：给事务通知起一个唯一标识
        * transaction-manager：给事务通知提供一个事务管理器引用
3. 配置AOP中的通用切入点表达式
4. 建立事务通知和切入点表达式的对应关系
5. 配置事务的属性tx:attributes
   * 属性: 
        * isolation：用于指定事务的隔离级别。默认值是DEFAULT，表示使用数据库的默认隔离级别。
        * propagation：用于指定事务的传播行为。默认值是REQUIRED，表示一定会有事务，增删改的选择。查询方法可以选择SUPPORTS。
        * read-only：用于指定事务是否只读。只有查询方法才能设置为true。默认值是false，表示读写。
        * timeout：用于指定事务的超时时间，默认值是-1，表示永不超时。如果指定了数值，以秒为单位。
        * rollback-for：用于指定一个异常，当产生该异常时，事务回滚，产生其他异常时，事务不回滚。没有默认值。表示任何异常都回滚。
        * no-rollback-for：用于指定一个异常，当产生该异常时，事务不回滚，产生其他异常时事务回滚。没有默认值。表示任何异常都回滚。

```
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
   xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
   xmlns:aop="http://www.springframework.org/schema/aop"
   xmlns:tx="http://www.springframework.org/schema/tx"
   xsi:schemaLocation="
    http://www.springframework.org/schema/beans
    http://www.springframework.org/schema/beans/spring-beans.xsd
    http://www.springframework.org/schema/tx
    http://www.springframework.org/schema/tx/spring-tx.xsd
    http://www.springframework.org/schema/aop
    http://www.springframework.org/schema/aop/spring-aop.xsd">

    <!-- 配置业务层-->
    <bean id="accountService" class="com.test.service.impl.AccountServiceImpl">
        <property name="accountDao" ref="accountDao"></property>
    </bean>

    <!-- 配置账户的持久层-->
    <bean id="accountDao" class="com.test.dao.impl.AccountDaoImpl">
        <property name="dataSource" ref="dataSource"></property>
    </bean>

    <!-- 配置数据源-->
    <bean id="dataSource" class="org.springframework.jdbc.datasource.DriverManagerDataSource">
        <property name="driverClassName" value="com.mysql.jdbc.Driver"></property>
        <property name="url" value="jdbc:mysql://localhost:3306/eesy"></property>
        <property name="username" value="root"></property>
        <property name="password" value="1234"></property>
    </bean>

    <!-- 配置事务管理器 -->
    <bean id="transactionManager" class="org.springframework.jdbc.datasource.DataSourceTransactionManager">
        <property name="dataSource" ref="dataSource"></property>
    </bean>

    <!-- 配置事务的通知-->
    <tx:advice id="txAdvice" transaction-manager="transactionManager">
        <!-- 配置事务的属性 -->
        <tx:attributes>
            <tx:method name="transfer" propagation="REQUIRED" read-only="false"/>
            <tx:method name="find*" propagation="SUPPORTS" read-only="true"></tx:method>
        </tx:attributes>
    </tx:advice>

    <!-- 配置aop-->
    <aop:config>
        <!-- 配置切入点表达式-->
        <aop:pointcut id="pt1" expression="execution(* com.test.service.impl.*.*(..))"></aop:pointcut>
        <!--建立切入点表达式和事务通知的对应关系 -->
        <aop:advisor advice-ref="txAdvice" pointcut-ref="pt1"></aop:advisor>
    </aop:config>

</beans>
```
