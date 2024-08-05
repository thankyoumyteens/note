# bean 的生命周期

BeanDefinition: spring 容器在进行实例化的时候, 会将 xml(或注解) 配置的 bean 信息封装成一个 BeanDefinition 对象, spring 根据 BeanDefinition 来创建 bean 对象。

BeanDefinition 中常用的字段:

- beanClassName: bean 的类名
- initMethodName: 初始化方法名
- propertyValues: bean 的属性值
- scope: bean 的作用域
- lazyInit: 延迟初始化

bean 的生命周期:

1. 调用构造方法创建 bean 对象
2. 依赖注入
3. 处理 Aware 接口: 比如 ApplicationContextAware
4. PostProcessor#before: 在 bean 的初始化之前调用, 用户可以加入自定义逻辑
5. 初始化: 实现 InitialzingBean 接口或者自定义 init 方法, 用户可以加入自定义逻辑
6. PostProcessor#after: 在 bean 的初始化之后调用, 用户可以加入自定义逻辑
7. 使用 bean
8. 销毁 bean
