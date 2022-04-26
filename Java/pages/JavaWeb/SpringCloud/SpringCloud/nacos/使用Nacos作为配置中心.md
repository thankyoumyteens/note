# 优先级

nacos配置大于本地jar中的application.properties配置，在nacos配置的参数肯定会覆盖jar配置，但一旦nacos不配置参数或参数被注释掉，本地jar的配置会生效。

nacos中微服务配置大于nacos中共享配置，比如s1微服务在nacos中配置的s1.properties与nacos共享配置有相同的参数，微服务只加载s1.properties中的参数，共享配置的相同参数会被覆盖。

nacos共享配置也大于本地jar中的application.properties配置，在本地jar的application.properties配置了和nacos共享配置相同的参数，微服务只加载nacos的共享配置。

# 开启认证

```
vim /nacos/conf/application.properties
```

```conf
### If turn on auth system:
nacos.core.auth.enabled=true
```

认证账号密码为nacos的登录账号密码

# 创建命名空间

菜单: 命名空间, 单击右上角的"新建命名空间"按钮

# 创建开发环境配置

配置管理->配置列表，单击右上角的+按钮，进入新建配置页面，填写配置信息

其中:
- Data ID: 填入 nacos-demo-dev.yml
- Group: 填入 team1
- 描述: 不填
- 配置内容: 要加载的配置内容，比如: username=wolf

# 创建测试环境配置

配置管理->配置列表，单击右上角的+按钮，进入新建配置页面，填写配置信息

其中:
- Data ID: 填入 nacos-demo-qa.yml
- Group: 填入 team1
- 描述: 不填
- 配置内容: 要加载的配置内容

# 创建共享配置

配置管理->配置列表，单击右上角的+按钮，进入新建配置页面，填写配置信息

其中:
- Data ID: 填入 team1-baseconfig.yml
- Group: 填入 team1
- 描述: 不填
- 配置内容: 要加载的配置内容

# 创建Java应用

创建一个Spring Boot应用

编辑pom.xml, 加入必要的依赖配置: 
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

创建配置文件bootstrap.yml, 并配置服务名称和Nacos地址

作为配置中心时，必须要使用bootstrap.yml，因为bootstrap.yml加载顺序优先于application.yml

```yml
spring:
  application:
    name: nacos-demo
  profiles:
    active: dev

# 使用Nacos配置 nacos-demo-dev.yml
spring:
  cloud:
    nacos:
      config:
        # 配置对应的分组
        group: team1
        # 命名空间
        namespace: dev
        # nacos的服务端地址
        server-addr: 127.0.0.1:8848
        # 配置文件格式
        file-extension: yml
        # Nacos 认证用户
        username: nacos
        # Nacos 认证密码
        password: 123456
        # 支持多个共享的配置
        shared-configs[0]:
          group: team1
          data-id: team1-baseconfig.yml
          # 是否动态刷新，默认为false
          refresh: true
  # 与spring.profiles.active匹配时启用
  profiles: dev

# 使用Nacos配置 nacos-demo-qa.yml
spring:
  cloud:
    nacos:
      config:
        group: team1
        namespace: qa
        server-addr: 127.0.0.1:8848
        file-extension: yml
        shared-configs[0]:
          group: team1
          data-id: team1-baseconfig.yml
          refresh: true
        shared-configs[1]:
          group: team2
          data-id: team2-baseconfig.yml
          refresh: true
  profiles: qa
```

启动应用

# Nacos配置加载规则

在Nacos Spring Cloud 中, dataID的格式如下: 
```
${prefix}-${spring.profile.active}.${file-extension}
```

- prefix: 默认为 spring.application.name的值，也可以通过配置项 spring.cloud.nacos.config.prefix来配置。
- spring.profile.active: 即当前环境对应的profile。
- 当 spring.profile.active 为空时，对应的连接符 - 也将不存在，dataId的拼接格式变成: ${prefix}.${file-extension}
- file-extension:  为配置文件的数据格式，可以通过设置项spring.cloud.nacos.config.file-extension来配置，默认值: properties。目前只支持 properties 和 yaml 类型。
- Group的值默认 DEFAULT_GROUP: 可以通过设置项 spring.cloud.nacos.config.group来配置，默认值:  DEFAULT_GROUP
