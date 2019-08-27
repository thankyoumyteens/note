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
<bean id="accountService" class="com.itheima.service.impl.AccountServiceImpl"/>
<!-- 配置 dao -->
<bean id="accountDao" class="com.itheima.dao.impl.AccountDaoImpl"/>

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
        class="com.itheima.service.impl.AccountServiceImpl"/>
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
        class="com.itheima.factory.StaticFactory"
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
        class="com.itheima.factory.InstanceFactory"/>
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
<bean id="accountService" class="com.itheima.service.impl.AccountServiceImpl">
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
<bean id="accountService" class="com.itheima.service.impl.AccountServiceImpl">
    <property name="name" value="test"/>
    <property name="age" value="21"/>
    <property name="birthday" ref="now"/>
</bean>
<bean id="now" class="java.util.Date"></bean>
```

## 注入集合

```
<bean id="accountService" class="com.itheima.service.impl.AccountServiceImpl">
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
    <context:component-scan base-package="com.itheima"/>
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
        <context:component-scan base-package="com.itheima"/>
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

