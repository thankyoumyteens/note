# Feign
Feign可以把Rest的请求进行隐藏, 伪装成类似SpringMVC的Controller一样。
Feign中已经自动集成了Ribbon, 因此不需要自己定义RestTemplate

# 导入依赖
```xml
<dependency>
	<groupId>org.springframework.cloud</groupId>
	<artifactId>spring-cloud-starter-openfeign</artifactId>
</dependency>
```

# Feign的客户端
Feign会通过动态代理, 自动生成实现类
```java
// 声明这是一个Feign客户端并指定服务名
@FeignClient("user-service")
public interface UserFeignClient {
	@GetMapping("/user/{id}")
	User queryUserById(@PathVariable("id") Long id);
}
```
改造原来的调用逻辑
```java
@Service
public class UserService {
	@Autowired
	private UserFeignClient userFeignClient;

	public List<User> queryUserById(Long id) {
		List<User> users = new ArrayList<>();
		return this.userFeignClient.queryUserById(id));
	}
}
```

# 开启Feign
启动类
```java
@SpringBootApplication
@EnableDiscoveryClient
@EnableHystrix
@EnableFeignClients // 开启Feign功能
public class UserConsumerDemoApplication {
	public static void main(String[] args) {
		SpringApplication.run(UserConsumerDemoApplication.class, args);
	}
}
```

# 负载均衡
Feign中本身已经集成了Ribbon依赖和自动配置
```yaml
user-service:
  ribbon:
    ConnectTimeout: 250 # 连接超时时间(ms)
    ReadTimeout: 1000 # 通信超时时间(ms)
    OkToRetryOnAllOperations: true # 是否对所有操作重试
    MaxAutoRetriesNextServer: 1 # 同一服务不同实例的重试次数
    MaxAutoRetries: 1 # 同一实例的重试次数
```

## Hystrix支持
Feign默认也有对Hystrix的集成
```yaml
feign:
  hystrix:
    enabled: true # 开启Feign的熔断功能
```

## 熔断处理
定义fallback
```java
@Component
public class UserFeignClientFallback implements UserFeignClient {
	@Override
	public User queryUserById(Long id) {
		User user = new User();
		user.setId(id);
		user.setName("用户查询出现异常！");
		return user;
	}
}
```
指定fallback
```java
@FeignClient(value = "user-service", fallback = UserFeignClientFallback.class)
public interface UserFeignClient {
	@GetMapping("/user/{id}")
	User queryUserById(@PathVariable("id") Long id);
}
```
