# 高可用

把 config-server 注册到 eureka 成为服务, 这样所有客户端就能以服务的方式进行访问。只需要启动多个指向同一 Git 仓库的 config-server 就能实现高可用了。

## Config Server 修改

1. 增加 eureka 依赖

```xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-netflix-eureka-client</artifactId>
</dependency>
```

2. application.yml 中指定注册中心

```yaml
eureka:
  client:
    # 服务注册中心的地址
    serviceUrl:
      defaultZone: http://localhost:27431/eureka/
```

3. 启动类开启服务发现

```java
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.client.discovery.EnableDiscoveryClient;
import org.springframework.cloud.config.server.EnableConfigServer;

@SpringBootApplication
// 开启配置中心功能
@EnableConfigServer
// 开启服务发现功能
@EnableDiscoveryClient
public class ConfigServerDemo {
    public static void main(String[] args) {
        SpringApplication.run(ConfigServerDemo.class, args);
    }
}
```

## Config Client 修改

1. 增加 eureka 依赖

```xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-netflix-eureka-client</artifactId>
</dependency>
```

2. bootstrap.yml

```yaml
eureka:
  client:
    # 服务注册中心的地址
    serviceUrl:
      defaultZone: http://localhost:27431/eureka/

spring:
  cloud:
    config:
      # 通过注册中心获取配置中心的地址
      discovery:
        enabled: true
        service-id: config-server-demo
      profile: dev
```

3. 启动类开启服务发现

```java
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.client.discovery.EnableDiscoveryClient;

@SpringBootApplication
// 开启服务发现功能
@EnableDiscoveryClient
public class ConfigClientDemo {
    public static void main(String[] args) {
        SpringApplication.run(ConfigClientDemo.class, args);
    }
}
```
