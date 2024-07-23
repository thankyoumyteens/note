# 自动配置原理

`@SpringBootApplication` 注解重要是由 3 个注解组成的:

1. `@SpringBootConfiguration`: 继承自 `@Configuration` 注解, 用来声明当前类是一个配置类
2. `@ComponentScan`: 组件扫描
3. `@EnableAutoConfiguration`: 实现自动配置的关键

`@EnableAutoConfiguration`注解内容如下:

```java
@Target(ElementType.TYPE)
@Retention(RetentionPolicy.RUNTIME)
@Documented
@Inherited
@AutoConfigurationPackage
@Import(AutoConfigurationImportSelector.class)
public @interface EnableAutoConfiguration {
    // ...
}
```

其中的 `@Import(AutoConfigurationImportSelector.class)` 会加载 `AutoConfigurationImportSelector` 类。

`AutoConfigurationImportSelector` 类实现了 `DeferredImportSelector` 接口, Spring 容器在启动时, 会在解析完其他所有项目中定义的配置类之后, 会调用 `selectImports` 方法, 然后把该方法返回的类名对应的类作为配置类进行解析。`AutoConfigurationImportSelector` 类的 `selectImports` 方法会读取当前项目和项目依赖的 jar 包的 classpath 路径下的 `META-INF/spring.factories` 文件。

`spring.factories` 文件中记录了配置类的类全名, 这些配置类会根据条件注解来决定是否需要加载到 spring 中。

比如 `RedisAutoConfiguration` 中就使用了 `@ConditionalOnClass({RedisOperations.class})` 注解来判断项目中是否引入了 `spring-boot-starter-data-redis` 依赖, 只有引入了才会加载。

```java
@AutoConfiguration
// 即项目中引入了 Spring Data Redis 后, 就会有这个类了
@ConditionalOnClass({RedisOperations.class})
// 导入在 application.properties 中配置的redis连接信息
@EnableConfigurationProperties({RedisProperties.class})
// 导入连接池信息（如果存在的话）
@Import({LettuceConnectionConfiguration.class, JedisConnectionConfiguration.class})
public class RedisAutoConfiguration {
    // ...
    @Bean
    @ConditionalOnMissingBean(
        name = {"redisTemplate"}
    )
    @ConditionalOnSingleCandidate(RedisConnectionFactory.class)
    public RedisTemplate<Object, Object> redisTemplate(RedisConnectionFactory redisConnectionFactory) {
        RedisTemplate<Object, Object> template = new RedisTemplate();
        template.setConnectionFactory(redisConnectionFactory);
        return template;
    }
    // ...
}
```
