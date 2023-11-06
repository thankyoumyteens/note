# BeanDefinition

BeanDefinition 是一个接口，是 bean 标签在 Spring 容器中的内部表示形式。

常用的 BeanDefinition 实现类：

- AbstractBeanDefinition：内部默认实现了 BeanDefinition 的绝大部分方法，对一些属性进行了默认值的赋值，其他的实现类基本上都是在 AbstractBeanDefinition 的基础上完成的
- RootBeanDefinition：它对应一般的 bean 标签
- ChildBeanDefinition：在配置文件中可以定义父 bean 标签和子 bean 标签，父 bean 用 RootBeanDefinition 表示，而子 bean 用 ChildBeanDefinition 表示，而没有父 bean 的 bean 标签就使用 RootBeanDefinition 表示
- GenericBeanDefinition：Spring2.5 以后新加入的 BeanDefinition 实现类，同时兼具 RootBeanDefinition 和 ChildBeanDefinition 的功能，自从有了 GenericBeanDefinition 之后，RootBeanDefinition 和 ChildBeanDefinition 相对就用的少了

AbstractBeanDefinition 中定义的字段对应了 bean 标签的属性和子标签：

```java
public abstract class AbstractBeanDefinition extends BeanMetadataAttributeAccessor
        implements BeanDefinition, Cloneable {

    // bean的作用范围，对应bean属性scope
    private String scope = SCOPE_DEFAULT;
    // 是否是抽象，对应bean属性abstract
    private boolean abstractFlag = false;
    // 是否延迟加载，对应bean属性lazy-init
    private boolean lazyInit = false;
    // 自动注人模式，对应bean属性autowire
    private int autowireMode = AUTOWIRE_NO;
    // 依赖检查，spring 3．0后弃用
    private int dependencyCheck = DEPENDENCY_CHECK_NONE;
    // 依赖其他bean，表示这个bean实例化前需要先实例化dependsOn中指定的bean
    // 对应bean属性depend-on
    private String[] dependsOn;
    // 设置当前bean在被其他对象作为自动注入对象的时候，是否作为候选bean，
    // 对应bean属性autowire-candidate
    private boolean autowireCandidate = true;
    // 自动注入时，当出现多个bean候选者时，将作为首选，对应bean属性primary
    private boolean primary = false;
    // 用于记录Qua1ifier，对应子标签qualifier
    private final Map<String, AutowireCandidateQualifier> qualifiers = new LinkedHashMap<>();
    // 允许访问非public的构造方法和普通方法，程序没置
    private boolean nonPublicAccessAllowed = true;
    // 是否以一种宽松的模式解析构造方法
    // 如果为false，则在如下情况抛出异常，因为spring无法准确定位哪个构造方法，程序设置
    /*
        interface Test {}
        class TestImpl implements Test {}

        class Main {
            Main(Test t) {}
            Main(TestImpl t) {}
        }
     */
    private boolean lenientConstructorResolution = true;
    // 对应bean属性 actory—bean
    private String factoryBeanName;
    // 对应bean属性 actory—method
    private String factoryMethodName;
    // 记录构造方法注入属性，对应bean属性constructor-arg
    private ConstructorArgumentValues constructorArgumentValues;
    // 普通属性集合
    private MutablePropertyValues propertyValues;
    // 记录lookup-method、replaced-method
    private MethodOverrides methodOverrides = new MethodOverrides();
    // 初始化方法，对应 bean 属性 init-method
    private String initMethodName;
    // 销毁方法，对应 bean 属性 destory-method
    private String destroyMethodName;
    // 是否执行 init-method ，程序设置
    private boolean enforceInitMethod = true;
    // 是否执行 destory-method. 程序设置
    private boolean enforceDestroyMethod = true;
    // 是否是用户定义的而不是应用程序本身定义的，创建AOP时候为true，程序设置
    private boolean synthetic = false;

    private int role = BeanDefinition.ROLE_APPLICATION;
    // bean 的描述信息
    private String description;
    // 这个 bean 定义的资源
    private Resource resource;
    // 是否是单例，取决于bean属性scope
    public boolean isSingleton() {
        return SCOPE_SINGLETON.equals(this.scope) || SCOPE_DEFAULT.equals(this.scope);
    }
    // 是否是prototype，取决于bean属性scope
    public boolean isPrototype() {
        return SCOPE_PROTOTYPE.equals(this.scope);
    }
}
```
