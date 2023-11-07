# BeanDefinitionParser 实现

1. 在 resources 下创建 META-INF 文件夹
2. 在 META-INF 下创建 person.xsd 文件：
   ```xml
   <?xml version="1.0" encoding="UTF-8"?>
   <!-- 自定义命名空间：http://test.demo/person -->
   <xsd:schema
           xmlns="http://test.demo/person"
           xmlns:xsd="http://www.w3.org/2001/XMLSchema"
           xmlns:beans="http://www.springframework.org/schema/beans"
           targetNamespace="http://test.demo/person"
           elementFormDefault="qualified"
           attributeFormDefault="unqualified">
       <xsd:import namespace="http://www.springframework.org/schema/beans"/>
       <xsd:element name="person">
           <xsd:complexType>
               <xsd:complexContent>
                   <!--identifiedType自动添加bean的 id 属性-->
                   <xsd:extension base="beans:identifiedType">
                       <xsd:attribute name="personName" type="xsd:string"/>
                       <xsd:attribute name="age" type="xsd:integer"/>
                   </xsd:extension>
               </xsd:complexContent>
           </xsd:complexType>
       </xsd:element>
   </xsd:schema>
   ```
3. 创建 person 标签的自定义解析器：

   ```java
   public class PersonParser implements BeanDefinitionParser {

       private final Class<?> beanclass;

       public PersonParser(Class<?> beanclass) {
           this.beanclass = beanclass;
       }

       public BeanDefinition parse(Element element, ParserContext parserContext) {
           RootBeanDefinition beanDefinition = new RootBeanDefinition();
           beanDefinition.setBeanClass(beanclass);
           beanDefinition.setLazyInit(false);
           // 解析自定义标签的属性
           String personName = element.getAttribute("personName");
           int age = Integer.parseInt(element.getAttribute("age"));
           beanDefinition.getPropertyValues().add("personName", personName);
           beanDefinition.getPropertyValues().add("age", age);
           // bean的注册中心
           BeanDefinitionRegistry beanDefinitionRegistry = parserContext.getRegistry();
           // 把bean注册到注册中心
           String id = element.getAttribute("id");
           beanDefinitionRegistry.registerBeanDefinition(id, beanDefinition);
           return beanDefinition;
       }
   }
   ```

4. 创建自定义命名空间的处理器：

   ```java
   public class MyNamespaceHandler extends NamespaceHandlerSupport {

       public void init() {
           // 为person标签指定解析器：PersonParser
           registerBeanDefinitionParser("person", new PersonParser(Person.class));
       }
   }
   ```

5. 在 META-INF 下创建 spring.handlers 文件(spring 遇到自定义标签时会来找这个文件)：
   ```conf
   # 指定自定义命名空间：http://test.demo/person 对应的处理器
   http\://test.demo/person=org.example.MyNamespaceHandler
   ```
6. 在 META-INF 下创建 spring.schemas 文件(spring 遇到自定义标签时会来找这个文件)：
   ```conf
   # 指定自定义命名空间：http://test.demo/person 对应的xsd
   http\://test.demo/person.xsd=META-INF/person.xsd
   ```
7. 创建 spring 的 xml 配置文件 testCusTag.xml：
   ```xml
   <?xml version="1.0" encoding="UTF-8"?>
   <beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xmlns:myTag="http://test.demo/person"
       xsi:schemaLocation="http://www.springframework.org/schema/beans
       http://www.springframework.org/schema/beans/spring-beans.xsd
           http://test.demo/person http://test.demo/person.xsd">
       <!-- 不使用bean标签创建bean -->
       <!-- 使用person标签创建bean -->
       <myTag:person id="p" personName="张三" age="15"/>
   </beans>
   ```
8. 测试：
   ```java
   public static void main(String[] args) {
       ApplicationContext context = new ClassPathXmlApplicationContext("testCusTag.xml");
       Person p = (Person) context.getBean("p");
       System.out.println(p);
   }
   ```
9. 输出：
   ```
   Person(personName=张三, age=15)
   ```
