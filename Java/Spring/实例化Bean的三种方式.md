# 使用默认无参构造函数
在默认情况下,它会根据默认无参构造函数来创建类对象。如果 bean 中没有默认无参构造函数, 将会创建失败
```xml
<bean id="accountService" 
  class="com.test.service.impl.AccountServiceImpl"/>
```
bean 标签的属性:
- id:给对象在容器中提供一个唯一标识。用于获取对象
- class:指定类的全限定类名。用于反射创建对象。默认情况下调用无参构造函数
- scope:指定对象的作用范围。singleton:默认值, 单例。prototype:多例

# 使用其他类的静态方法创建对象
使用 StaticFactory 类中的静态方法 createAccountService 创建对象, 并存入 spring 容器
-->
```xml
<bean id="accountService"
  class="com.test.factory.StaticFactory"
  factory-method="createAccountService"/>
```
bean 标签的属性:
- id 属性:指定 bean 的 id, 用于从容器中获取
- class 属性:指定静态工厂的全限定类名
- factory-method 属性:指定生产对象的静态方法

# 使用其他对象的方法创建对象
先把工厂的创建交给 spring 来管理。然后在使用工厂的 bean 来调用里面的方法
```xml
<bean id="instancFactory" 
  class="com.test.factory.InstanceFactory"/>
<bean id="accountService"
  factory-bean="instancFactory"
  factory-method="createAccountService"/>
```
bean 标签的属性:
- factory-bean 属性:用于指定实例工厂 bean 的 id。
- factory-method 属性:用于指定实例工厂中创建对象的方法。
