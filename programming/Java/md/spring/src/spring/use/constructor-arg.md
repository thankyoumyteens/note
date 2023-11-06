# constructor-arg

constructor-arg 用来指定创建对象时使用哪个构造方法，每一个 constructor-arg 子标签配置一个参数列表中的参数值。如果不配置 constructor-arg 子标签，则默认使用无参构造方法实例化对象。

constructor-arg 标签属性：

- name 属性：通过参数名找到参数列表中对应参数
- index 属性：通过索引找到参数列表中对应参数，index 从 0 开始
- type 属性：通过类型找到参数列表中对应参数
- value 属性：设置参数对应的值，用于设定基本数据类型和 String 类型的数据
- ref 属性：如果参数值为非基本数据类型，则可通过 ref 为参数注入值，其值为另一个 bean 标签的 id 或 name

constructor-arg 的子标签：

- ref 子标签：对应 ref 属性，该标签 name 属性的属性值为另一个 bean 标签 id 或 name 属性的属性值
- value 子标签：对应 value 属性,用于设置基本数据类型或 String 类型的参数值
- list 子标签：为数组或 List 类型的参数赋值
- set 子标签：为 Set 集合类型参数赋值
- map 子标签：为 Map 集合类型参数赋值
- props 子标签：为 Properties 类型的参数赋值

## 用法

```java
public class Student {

    public Student() {
        System.out.println("OK");
    }
    public Student(int age) {
        System.out.println("age="+age);
    }
    public Student(String name) {
        System.out.println("name="+name);
    }
    public Student(int age,String name) {
        System.out.println("age="+age+",name="+name);
    }
    public Student(Date now) {
        System.out.println("现在的时间是："+now);
    }
    public Student(List<Object> list) {
        for (Object object : list) {
            System.out.println(object);
        }
    }
    public Student(Object [] array) {
        for (Object object : array) {
            System.out.println(object);
        }
    }
    public Student(Set<Object> set) {
        for(Object object : set) {
            System.out.println(object);
        }
    }
    public Student(Map<String,Object> map) {
        Set<String> keys = map.keySet();
        for (String key : keys) {
            System.out.println(key+":"+map.get(key));
        }
    }
    public Student(Properties properties) {
        System.out.println(properties.get("driver"));
        System.out.println(properties.get("userName"));
        System.out.println(properties.get("password"));
        System.out.println(properties.get("url"));
    }
}
```

调用`Student(int age,String name)`构造方法：

```xml
<!-- 按参数顺序排列 -->
<bean class="test.Student">
    <constructor-arg value="12"></constructor-arg>
    <constructor-arg value="张三"></constructor-arg>
</bean>
<!-- 使用name属性 -->
<bean class="test.Student">
    <constructor-arg name="name" value="张三"></constructor-arg>
    <constructor-arg name="age" value="12"></constructor-arg>
</bean>
<!-- 使用index属性 -->
<bean class="test.Student">
    <!-- index为参数列表中参数的顺序，从0开始 -->
    <constructor-arg index="1" value="张三"></constructor-arg>
    <constructor-arg index="0" value="12"></constructor-arg>
</bean>
<!-- 使用type属性 -->
<bean class="test.Student">
    <!-- 这里int不可以是java.lang.Integer，要和参数数据类型严格一致 -->
    <constructor-arg type="int" value="12"></constructor-arg>
    <constructor-arg type="java.lang.String" value="张三"></constructor-arg>
</bean>
```

调用`Student(Date now)`构造方法：

```xml
<bean class="java.util.Date" id="d"></bean>
<bean class="test.Student">
    <constructor-arg ref="d"></constructor-arg>
</bean>
```

调用`Student(Object [] array)`构造方法：

```xml
<bean class="test.Student">
    <constructor-arg>
        <array>
            <value>18</value>
            <value>Rechel</value>
            <ref bean="d"/>
            <bean class="java.lang.String">
                <constructor-arg value="String"></constructor-arg>
            </bean>
        </array>
    </constructor-arg>
</bean>
```

调用`Student(List<Object> list)`构造方法：

```xml
<bean class="test.Student">
    <constructor-arg>
        <list>
            <value>12</value>
            <value>Tomcat</value>
            <ref bean="d"/>
            <bean class="java.lang.String">
                <constructor-arg value="This is a list"></constructor-arg>
            </bean>
        </list>
    </constructor-arg>
</bean>
```

调用`Student(Set<Object> set)`构造方法：

```xml
<bean class="test.Student">
    <constructor-arg>
        <set>
            <value>12</value>
            <value>Tomcat</value>
            <ref bean="d"/>
            <bean class="java.lang.String">
                <constructor-arg value="This is a set"></constructor-arg>
            </bean>
        </set>
    </constructor-arg>
</bean>
```

调用`Student(Map<String,Object> map)`构造方法：

```xml
<bean class="test.Student">
    <constructor-arg>
        <map>
            <entry key="name" value="myself"></entry>
            <entry key="age" value="22"></entry>
            <entry key="now" value-ref="da"></entry>
        </map>
    </constructor-arg>
</bean>
```

调用`Student(Properties properties)`构造方法：

```xml
<bean class="test.Student">
    <constructor-arg>
        <props>
            <prop key="driver">com.mysql.jdbc.Driver</prop>
            <prop key="userName">root</prop>
            <prop key="password">root</prop>
            <prop key="url">jdbc:mysql://127.0.0.1:3306/test</prop>
        </props>
    </constructor-arg>
</bean>
```
