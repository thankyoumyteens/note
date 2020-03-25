# Eureka注册中心
Eureka负责管理、记录服务提供者的信息。服务调用者无需自己寻找服务, 而是把自己的需求告诉Eureka, 然后Eureka会把符合你需求的服务告诉你。服务提供方与Eureka之间通过"心跳"机制进行监控, 当某个服务提供方出现问题, Eureka自然会把它从服务列表中剔除。
这就实现了服务的自动注册、发现、状态监控。
- Eureka是服务注册中心(可以是一个集群), 对外暴露自己的地址
- 服务提供者启动后向Eureka注册自己信息(地址, 提供什么服务)
- 服务消费者向Eureka订阅服务, Eureka会将对应服务的所有提供者地址列表发送给消费者, 并且定期更新
- 服务提供者定期通过http方式向Eureka刷新自己的状态
- 服务消费者通过从Eureka获得的地址调用服务提供者

# 注册中心
依赖
```xml
<!-- Eureka服务端 -->
<dependency>
	<groupId>org.springframework.cloud</groupId>
	<artifactId>spring-cloud-starter-netflix-eureka-server</artifactId>
</dependency>
```
启动类
```java
@SpringBootApplication
@EnableEurekaServer // 声明这个应用是一个EurekaServer
public class EurekaDemoApplication {
	public static void main(String[] args) {
		SpringApplication.run(EurekaDemoApplication.class, args);
	}
}
```
配置
```yaml
server:
  port: 10086
spring:
  application:
    name: eureka-server # 应用名称, 会在Eureka中显示
eureka:
	client:
		# 是否注册自己的信息到EurekaServer, 默认是true
    register-with-eureka: false 
		# 是否拉取其它服务的信息, 默认是true
		fetch-registry: false 
    service-url: # EurekaServer的地址
      defaultZone: http://127.0.0.1:${server.port}/eureka
```
# 服务提供方
依赖
```xml
<!-- Eureka客户端 -->
<dependency>
	<groupId>org.springframework.cloud</groupId>
	<artifactId>spring-cloud-starter-netflix-eureka-client</artifactId>
</dependency>
```
启动类
```java
@SpringBootApplication
@EnableDiscoveryClient // 开启EurekaClient
public class UserServiceDemoApplication {
	public static void main(String[] args) {
		SpringApplication.run(UserServiceDemoApplication.class, args);
	}
}
```
配置
```yaml
server:
  port: 8081
spring:
  datasource:
    # 省略
  application:
    name: user-service # 应用的id
mybatis:
  type-aliases-package: com.demo.pojo
eureka:
  client:
    service-url: # EurekaServer地址
      defaultZone: http://127.0.0.1:10086/eureka
	instance:
		 # 当调用getHostname获取实例的hostname时, 返回ip而不是host名称
    prefer-ip-address: true
    ip-address: 127.0.0.1 # 指定自己的ip信息
```

# 服务消费者
依赖
```xml
<!-- Eureka客户端 -->
<dependency>
	<groupId>org.springframework.cloud</groupId>
	<artifactId>spring-cloud-starter-netflix-eureka-client</artifactId>
</dependency>
```
启动类
```java
@SpringBootApplication
@EnableDiscoveryClient // 开启Eureka客户端
public class UserConsumerDemoApplication {
    @Bean
    public RestTemplate restTemplate() {
        return new RestTemplate(new OkHttp3ClientHttpRequestFactory());
    }
    public static void main(String[] args) {
        SpringApplication.run(UserConsumerDemoApplication.class, args);
    }
}
```
配置
```yaml
server:
  port: 8080
spring:
  application:
    name: consumer # 应用名称
eureka:
  client:
    service-url: # EurekaServer地址
      defaultZone: http://127.0.0.1:10086/eureka
	instance:
		# 当其它服务获取地址时提供ip而不是hostname
    prefer-ip-address: true 
    ip-address: 127.0.0.1 # 指定自己的ip信息
```
根据服务名称, 获取服务实例
```java
@Service
public class UserService {
	@Autowired
	private RestTemplate restTemplate;
	// Eureka客户端, 可以获取到服务实例信息
	@Autowired
	private DiscoveryClient discoveryClient;

	public User queryUserById(Long id) {
		// 根据服务名称, 获取服务实例
		List<ServiceInstance> instances = discoveryClient.getInstances("user-service");
		ServiceInstance instance = instances.get(0);
		// 获取ip和端口信息
		String baseUrl = "http://"+instance.getHost() + ":" + instance.getPort()+"/user/";
		User user = this.restTemplate.getForObject(baseUrl + id, User.class));
		return user;
	}
}
```

# Eureka Server集群
多个Eureka Server之间也会互相注册为服务, 当服务提供者注册到Eureka Server集群中的某个节点时, 该节点会把服务的信息同步给集群中的每个节点, 从而实现数据同步。因此, 无论客户端访问到Eureka Server集群中的任意一个节点, 都可以获取到完整的服务列表信息。

## EurekaServer

假设要搭建两条EurekaServer的集群, 端口分别为: 10086和10087

修改原来的EurekaServer配置: 
```yaml
server:
  port: 10086 # 端口
spring:
  application:
    name: eureka-server # 应用名称, 会在Eureka中显示
eureka:
  client:
    service-url: # 配置其他Eureka服务的地址, 而不是自己, 比如10087
      defaultZone: http://127.0.0.1:10087/eureka
```
另外一台配置恰好相反: 
```yaml
server:
  port: 10087 # 端口
spring:
  application:
    name: eureka-server # 应用名称, 会在Eureka中显示
eureka:
  client:
    service-url: # 配置其他Eureka服务的地址, 而不是自己, 比如10087
      defaultZone: http://127.0.0.1:10086/eureka
```

## 客户端注册服务到集群
```yaml
eureka:
  client:
    service-url: # EurekaServer地址,多个地址以','隔开
      defaultZone: http://127.0.0.1:10086/eureka,http://127.0.0.1:10087/eureka
```
