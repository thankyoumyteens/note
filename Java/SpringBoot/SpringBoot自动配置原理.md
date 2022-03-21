启动类中有@SpringBootApplication注解，@SpringBootApplication注解中有@EnableAutoConfiguration注解，@EnableAutoConfiguration注解中有@Import(AutoConfigurationImportSelector.class)注解。

AutoConfigurationImportSelector这个类中的getCandidateConfigurations()方法里面通过SpringFactoriesLoader.loadFactoryNames()扫描所有具有META-INF/spring.factories文件的jar包。

spring-boot-autoconfigure-版本号.jar中的spring.factories文件指定了redis、mq等springboot内置的配置类。

getCandidateConfigurations()方法加载完成后，过滤掉重复的配置类和在@SpringBootApplication(exclude = {})中指定的配置类。

在剩下的配置类中实例化@Conditional注解为true的bean。@Conditional注解（如：@ConditionalOnBean：当容器里有指定Bean的条件下）可以组合使用。

## spring.factories例子

```ini
# 多个类名逗号分隔,而\表示忽略换行
org.springframework.boot.autoconfigure.EnableAutoConfiguration=\
org.demo.Demo1AutoConfiguration,\
org.demo.Demo2AutoConfiguration
```

## 配置类例子

```java
@Bean
// 当SpringIoc容器内不存在指定Bean的条件
@ConditionalOnMissingBean
public DemoBean demoBean(t) {
   return new DemoBean();
}
```
