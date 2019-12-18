# Eureka注册中心

## 认识Eureka

在刚才的案例中, user-service对外提供服务, 需要对外暴露自己的地址。而consumer(调用者)需要记录服务提供者的地址。将来地址出现变更, 还需要及时更新。这在服务较少的时候并不觉得有什么, 但是在现在日益复杂的互联网环境, 一个项目肯定会拆分出十几, 甚至数十个微服务。此时如果还人为管理地址, 不仅开发困难, 将来测试、发布上线都会非常麻烦, 这与DevOps的思想是背道而驰的。

Eureka负责管理、记录服务提供者的信息。服务调用者无需自己寻找服务, 而是把自己的需求告诉Eureka, 然后Eureka会把符合你需求的服务告诉你。

同时, 服务提供方与Eureka之间通过`心跳`机制进行监控, 当某个服务提供方出现问题, Eureka自然会把它从服务列表中剔除。

这就实现了服务的自动注册、发现、状态监控。

### 基本架构: 

 ![1525597885059](img/1525597885059.png)

- Eureka: 就是服务注册中心(可以是一个集群), 对外暴露自己的地址
- 提供者: 启动后向Eureka注册自己信息(地址, 提供什么服务)
- 消费者: 向Eureka订阅服务, Eureka会将对应服务的所有提供者地址列表发送给消费者, 并且定期更新
- 心跳(续约): 提供者定期通过http方式向Eureka刷新自己的状态

## 入门案例

### 编写EurekaServer

接下来我们创建一个项目, 启动一个EurekaServer: 

依然使用spring提供的快速搭建工具: 

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" 
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
	xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 
   http://maven.apache.org/xsd/maven-4.0.0.xsd">
	<modelVersion>4.0.0</modelVersion>

	<groupId>com.demo</groupId>
	<artifactId>eureka-demo</artifactId>
	<version>0.0.1-SNAPSHOT</version>
	<packaging>jar</packaging>

	<name>eureka-demo</name>
	<description>Demo project for Spring Boot</description>

	<parent>
		<groupId>org.springframework.boot</groupId>
		<artifactId>spring-boot-starter-parent</artifactId>
		<version>2.0.1.RELEASE</version>
		<relativePath/> <!-- lookup parent from repository -->
	</parent>

	<properties>
		<project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
		<project.reporting.outputEncoding>UTF-8</project.reporting.outputEncoding>
		<java.version>1.8</java.version>
    <!-- SpringCloud版本, 是最新的F系列 -->
		<spring-cloud.version>Finchley.RC1</spring-cloud.version>
	</properties>

	<dependencies>
    <!-- Eureka服务端 -->
		<dependency>
			<groupId>org.springframework.cloud</groupId>
			<artifactId>spring-cloud-starter-netflix-eureka-server</artifactId>
		</dependency>
	</dependencies>

	<dependencyManagement>
		<dependencies>
      <!-- SpringCloud依赖, 一定要放到dependencyManagement中, 起到管理版本的作用即可 -->
			<dependency>
				<groupId>org.springframework.cloud</groupId>
				<artifactId>spring-cloud-dependencies</artifactId>
				<version>${spring-cloud.version}</version>
				<type>pom</type>
				<scope>import</scope>
			</dependency>
		</dependencies>
	</dependencyManagement>

	<build>
		<plugins>
			<plugin>
				<groupId>org.springframework.boot</groupId>
				<artifactId>spring-boot-maven-plugin</artifactId>
			</plugin>
		</plugins>
	</build>

	<repositories>
		<repository>
			<id>spring-milestones</id>
			<name>Spring Milestones</name>
			<url>https://repo.spring.io/milestone</url>
			<snapshots>
				<enabled>false</enabled>
			</snapshots>
		</repository>
	</repositories>
</project>
```

编写启动类: 
```java
@SpringBootApplication
@EnableEurekaServer // 声明这个应用是一个EurekaServer
public class EurekaDemoApplication {

	public static void main(String[] args) {
		SpringApplication.run(EurekaDemoApplication.class, args);
	}
}
```

编写配置: 
```yaml
server:
  port: 10086 # 端口
spring:
  application:
    name: eureka-server # 应用名称, 会在Eureka中显示
eureka:
  client:
    register-with-eureka: false # 是否注册自己的信息到EurekaServer, 默认是true
    fetch-registry: false # 是否拉取其它服务的信息, 默认是true
    service-url: # EurekaServer的地址, 现在是自己的地址, 如果是集群, 需要加上其它Server的地址。
      defaultZone: http://127.0.0.1:${server.port}/eureka

```

启动服务, 并访问eureka管理面板: http://127.0.0.1:10086/eureka

### 将user-service注册到Eureka

注册服务, 就是在服务上添加Eureka的客户端依赖, 客户端代码会自动把服务注册到EurekaServer中。

先添加SpringCloud依赖: 
```xml
<!-- SpringCloud的依赖 -->
<dependencyManagement>
    <dependencies>
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-dependencies</artifactId>
            <version>Finchley.RC1</version>
            <type>pom</type>
            <scope>import</scope>
        </dependency>
    </dependencies>
</dependencyManagement>
<!-- Spring的仓库地址 -->
<repositories>
    <repository>
        <id>spring-milestones</id>
        <name>Spring Milestones</name>
        <url>https://repo.spring.io/milestone</url>
        <snapshots>
            <enabled>false</enabled>
        </snapshots>
    </repository>
</repositories>
```

然后是Eureka客户端: 

```xml
<!-- Eureka客户端 -->
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-netflix-eureka-client</artifactId>
</dependency>
```

在启动类上开启Eureka客户端功能
```java
@SpringBootApplication
@EnableDiscoveryClient // 开启EurekaClient功能
public class UserServiceDemoApplication {
	public static void main(String[] args) {
		SpringApplication.run(UserServiceDemoApplication.class, args);
	}
}
```

编写配置
```yaml
server:
  port: 8081
spring:
  datasource:
    url: jdbc:mysql://localhost:3306/mydb01
    username: root
    password: 123
    hikari:
      maximum-pool-size: 20
      minimum-idle: 10
  application:
    name: user-service # 应用名称
mybatis:
  type-aliases-package: com.demo.pojo
eureka:
  client:
    service-url: # EurekaServer地址
      defaultZone: http://127.0.0.1:10086/eureka
  instance:
    prefer-ip-address: true # 当调用getHostname获取实例的hostname时, 返回ip而不是host名称
    ip-address: 127.0.0.1 # 指定自己的ip信息, 不指定的话会自己寻找
```

注意: 
- 这里我们添加了spring.application.name属性来指定应用名称, 将来会作为应用的id使用。
- 不用指定register-with-eureka和fetch-registry, 因为默认是true

重启项目, 访问Eureka监控页面(http://127.0.0.1:10086/eureka)查看

发现user-service服务已经注册成功了

### 消费者从Eureka获取服务

接下来我们修改consumer-demo, 尝试从EurekaServer获取服务。

方法与消费者类似, 只需要在项目中添加EurekaClient依赖, 就可以通过服务名称来获取信息了！

先添加SpringCloud依赖: 
```xml
<!-- SpringCloud的依赖 -->
<dependencyManagement>
    <dependencies>
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-dependencies</artifactId>
            <version>Finchley.RC1</version>
            <type>pom</type>
            <scope>import</scope>
        </dependency>
    </dependencies>
</dependencyManagement>
<!-- Spring的仓库地址 -->
<repositories>
    <repository>
        <id>spring-milestones</id>
        <name>Spring Milestones</name>
        <url>https://repo.spring.io/milestone</url>
        <snapshots>
            <enabled>false</enabled>
        </snapshots>
    </repository>
</repositories>
```

然后是Eureka客户端: 
```xml
<!-- Eureka客户端 -->
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-netflix-eureka-client</artifactId>
</dependency>
```

在启动类开启Eureka客户端
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

3)修改配置: 
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
    prefer-ip-address: true # 当其它服务获取地址时提供ip而不是hostname
    ip-address: 127.0.0.1 # 指定自己的ip信息, 不指定的话会自己寻找
```

修改代码, 用DiscoveryClient类的方法, 根据服务名称, 获取服务实例: 
```java
@Service
public class UserService {

    @Autowired
    private RestTemplate restTemplate;
    @Autowired
    private DiscoveryClient discoveryClient;// Eureka客户端, 可以获取到服务实例信息

    public List<User> queryUserByIds(List<Long> ids) {
        List<User> users = new ArrayList<>();
        // String baseUrl = "http://localhost:8081/user/";
        // 根据服务名称, 获取服务实例
        List<ServiceInstance> instances = discoveryClient.getInstances("user-service");
        // 因为只有一个UserService,因此我们直接get(0)获取
        ServiceInstance instance = instances.get(0);
        // 获取ip和端口信息
        String baseUrl = "http://"+instance.getHost() + ":" + instance.getPort()+"/user/";
        ids.forEach(id -> {
            // 我们测试多次查询, 
            users.add(this.restTemplate.getForObject(baseUrl + id, User.class));
            // 每次间隔500毫秒
            try {
                Thread.sleep(500);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        });
        return users;
    }
}
```

## 基础架构

Eureka架构中的三个核心角色: 

- 服务注册中心: Eureka的服务端应用, 提供服务注册和发现功能, 就是刚刚我们建立的eureka-demo
- 服务提供者: 提供服务的应用, 可以是SpringBoot应用, 也可以是其它任意技术实现, 只要对外提供的是Rest风格服务即可。本例中就是我们实现的user-service-demo
- 服务消费者: 消费应用从注册中心获取服务列表, 从而得知每个服务方的信息, 知道去哪里调用服务方。本例中就是我们实现的consumer-demo

## 高可用的Eureka Server

Eureka Server即服务的注册中心, 在刚才的案例中, 我们只有一个EurekaServer, 事实上EurekaServer也可以是一个集群, 形成高可用的Eureka中心。

### 服务同步

多个Eureka Server之间也会互相注册为服务, 当服务提供者注册到Eureka Server集群中的某个节点时, 该节点会把服务的信息同步给集群中的每个节点, 从而实现数据同步。因此, 无论客户端访问到Eureka Server集群中的任意一个节点, 都可以获取到完整的服务列表信息。

### 动手搭建高可用的EurekaServer

我们假设要搭建两条EurekaServer的集群, 端口分别为: 10086和10087

我们修改原来的EurekaServer配置: 
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

所谓的高可用注册中心, 其实就是把EurekaServer自己也作为一个服务进行注册, 这样多个EurekaServer之间就能互相发现对方, 从而形成集群。因此我们做了以下修改: 

- 删除了register-with-eureka=false和fetch-registry=false两个配置。因为默认值是true, 这样就会吧自己注册到注册中心了。
- 把service-url的值改成了另外一台EurekaServer的地址, 而不是自己

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

客户端注册服务到集群

因为EurekaServer不止一个, 因此注册服务的时候, service-url参数需要变化: 
```yaml
eureka:
  client:
    service-url: # EurekaServer地址,多个地址以','隔开
      defaultZone: http://127.0.0.1:10086/eureka,http://127.0.0.1:10087/eureka
```

### 服务提供者

服务提供者要向EurekaServer注册服务, 并且完成服务续约等工作。

服务提供者在启动时, 会检测配置属性中的: `eureka.client.register-with-erueka=true`参数是否正确, 事实上默认就是true。如果值确实为true, 则会向EurekaServer发起一个Rest请求, 并携带自己的元数据信息, Eureka Server会把这些信息保存到一个双层Map结构中。第一层Map的Key就是服务名称, 第二层Map的key是服务的实例id。

在注册服务完成以后, 服务提供者会维持一个心跳(定时向EurekaServer发起Rest请求), 告诉EurekaServer: “我还活着”。这个我们称为服务的续约(renew)；

有两个重要参数可以修改服务续约的行为: 
```yaml
eureka:
  instance:
    lease-expiration-duration-in-seconds: 90
    lease-renewal-interval-in-seconds: 30
```

- lease-renewal-interval-in-seconds: 服务续约(renew)的间隔, 默认为30秒
- lease-expiration-duration-in-seconds: 服务失效时间, 默认值90秒

也就是说, 默认情况下每个30秒服务会向注册中心发送一次心跳, 证明自己还活着。如果超过90秒没有发送心跳, EurekaServer就会认为该服务宕机, 会从服务列表中移除, 这两个值在生产环境不要修改, 默认即可。

但是在开发时, 这个值有点太长了, 经常我们关掉一个服务, 会发现Eureka依然认为服务在活着。所以我们在开发阶段可以适当调小。

```yaml
eureka:
  instance:
    lease-expiration-duration-in-seconds: 10 # 10秒即过期
    lease-renewal-interval-in-seconds: 5 # 5秒一次心跳
```

先来看一下服务状态信息: 

在Eureka监控页面, 查看服务注册信息: 

![1525617060656](img/1525617060656.png)

在status一列中, 显示以下信息: 

- UP(1): 代表现在是启动了1个示例, 没有集群
- DESKTOP-2MVEC12:user-service:8081: 是示例的名称(instance-id), 
- 默认格式是: `${hostname} + ${spring.application.name} + ${server.port}`
- instance-id是区分同一服务的不同实例的唯一标准, 因此不能重复。

我们可以通过instance-id属性来修改它的构成: 
```yaml
eureka:
  instance:
    instance-id: ${spring.application.name}:${server.port}
```

### 服务消费者

当服务消费者启动时, 会检测`eureka.client.fetch-registry=true`参数的值, 如果为true, 则会从Eureka Server服务的列表只读备份, 然后缓存在本地。并且`每隔30秒`会重新获取并更新数据。我们可以通过下面的参数来修改: 

```yaml
eureka:
  client:
    registry-fetch-interval-seconds: 5
```

生产环境中, 我们不需要修改这个值。

但是为了开发环境下, 能够快速得到服务的最新状态, 我们可以将其设置小一点。

### 失效剔除

有些时候, 我们的服务提供方并不一定会正常下线, 可能因为内存溢出、网络故障等原因导致服务无法正常工作。Eureka Server需要将这样的服务剔除出服务列表。因此它会开启一个定时任务, 每隔60秒对所有失效的服务(超过90秒未响应)进行剔除。

可以通过`eureka.server.eviction-interval-timer-in-ms`参数对其进行修改, 单位是毫秒, 生成环境不要修改。

这个会对我们开发带来极大的不变, 你对服务重启, 隔了60秒Eureka才反应过来。开发阶段可以适当调整, 比如10S

### 自我保护

我们关停一个服务, 就会在Eureka面板看到一条警告

这是触发了Eureka的自我保护机制。当一个服务未按时进行心跳续约时, Eureka会统计最近15分钟心跳失败的服务实例的比例是否超过了85%。在生产环境下, 因为网络延迟等原因, 心跳失败实例的比例很有可能超标, 但是此时就把服务剔除列表并不妥当, 因为服务可能没有宕机。Eureka就会把当前实例的注册信息保护起来, 不予剔除。生产环境下这很有效, 保证了大多数服务依然可用。

但是这给我们的开发带来了麻烦,  因此开发阶段我们都会关闭自我保护模式: 

```yaml
eureka:
  server:
    enable-self-preservation: false # 关闭自我保护模式(缺省为打开)
    eviction-interval-timer-in-ms: 1000 # 扫描失效服务的间隔时间(缺省为60*1000ms)
```
