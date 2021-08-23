# Nacos

Nacos 支持基于 DNS 和基于 RPC 的服务发现（可以作为springcloud的注册中心）、动态配置服务（可以做配置中心）、动态 DNS 服务。

# 创建配置

进入Nacos的控制页面，在配置列表功能页面中，单击右上角的+按钮，进入新建配置页面，填写配置信息

其中：
- Data ID： 填入 alibaba-nacos-config-client.properties
- Group： 使用默认值 DEFAULT_GROUP
- 描述：可不填
- 配置格式： 选择 Properties
- 配置内容： 应用要加载的配置内容，比如： username=wolf

# 创建应用

创建一个Spring Boot应用,命名为：alibaba-nacos-config-client

编辑pom.xml, 加入必要的依赖配置：
```xml
<parent>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-parent</artifactId>
    <version>2.0.5.RELEASE</version>
    <relativePath/>
</parent>
 
<dependencyManagement>
    <dependencies>
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-dependencies</artifactId>
            <version>Finchley.SR1</version>
            <type>pom</type>
            <scope>import</scope>
        </dependency>
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-alibaba-dependencies</artifactId>
            <version>0.2.2.RELEASE</version>
            <type>pom</type>
            <scope>import</scope>
        </dependency>
    </dependencies>
</dependencyManagement>
 
<dependencies>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-web</artifactId>
    </dependency>
    <dependency>
        <groupId>org.springframework.cloud</groupId>
        <artifactId>spring-cloud-starter-alibaba-nacos-config</artifactId>
    </dependency>
    <dependency>
        <groupId>org.projectlombok</groupId>
        <artifactId>lombok</artifactId>
        <version>1.18.2</version>
        <optional>true</optional>
    </dependency>
</dependencies>
```

创建应用主类和测试Controller

```java
@SpringBootApplication
public class NacosConfigClientApplication {
 
    public static void main(String[] args) {
        SpringApplication.run(NacosConfigClientApplication.class, args);
    }
}
```

```java
@Slf4j
@RestController
// 实现配置、实例热加载
@RefreshScope
public class TestController {
 
    @Value("${username}")
    private String username;
 
    @GetMapping("/test")
    public String hello() {
        return username;
    }
}
```

创建配置文件bootstrap.properties，并配置服务名称和Nacos地址
```yml
spring:
  application:
    name: alibaba-nacos-config-client
  profiles:
    active: dev

# spring.application.name值必须和Nacos配置中 Data ID 相同
spring:
  cloud:
    nacos:
      config:
        group: team1
        namespace: dev
        server-addr: 127.0.0.1:8848 # nacos的服务端地址
        file-extension: yml # 配置文件格式
        shared-configs[0]:
          group: team1
          data-id: team1-baseconfig.yml
          refresh: true
  profiles: dev

spring:
  cloud:
    nacos:
      config:
        group: team1
        namespace: qa
        server-addr: 127.0.0.1:8848 # nacos的服务端地址
        file-extension: yml # 配置文件格式
        shared-configs[0]:
          group: team1
          data-id: team1-baseconfig.yml
          refresh: true
  profiles: qa

```

启动应用

# Nacos配置加载规则

在Nacos Spring Cloud 中， dataID的完成格式如下：
```
${prefix}-${spring.profile.active}.${file-extension}
```
- prefix：默认为 spring.application.name的值，也可以通过配置项 spring.cloud.nacos.config.prefix来配置。
- spring.profile.active：即当前环境对应的profile。
- 当 spring.profile.active 为空时，对应的连接符 - 也将不存在，dataId的拼接格式变成：${prefix}.${file-extension}
- file-extension： 为配置文件的数据格式，可以通过设置项spring.cloud.nacos.config.file-extension来配置，默认值：properties。目前只支持 properties 和 yaml 类型。
- Group的值默认 DEFAULT_GROUP: 可以通过设置项 spring.cloud.nacos.config.group来配置，默认值： DEFAULT_GROUP
