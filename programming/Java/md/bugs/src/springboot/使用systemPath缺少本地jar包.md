# 使用 systemPath 缺少本地 jar 包

在使用 Maven 的时候, 如果我们要依赖一个本地的 jar 包的时候, 通常都会使用`<scope>system</scope>`和`<systemPath></systemPath>`来处理。
例如: 

```xml
//引用本地jar包
<dependency>
    <groupId>com.mytest</groupId>
    <artifactId>test</artifactId>
    <version>1.0</version>
    <scope>system</scope>
    <systemPath>${pom.basedir}/lib/test-1.0.jar</systemPath>
</dependency>
```

如果你仅仅是这么做了, 在你使用 SpringBoot 打包插件生成 jar 包的时候, 你会发现这个 jar 包不会被打进去, 进而出现错误。
这个就需要在 maven 插接中配置一个 includeSystemScope 属性: 

```xml
<plugin>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-maven-plugin</artifactId>
    <configuration>
    	<!--设置为true, 以便把本地的system的jar也包括进来-->
        <includeSystemScope>true</includeSystemScope>
    </configuration>
</plugin>
```
