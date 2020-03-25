# Hystrix
- 正常工作的情况下, 客户端请求调用服务API接口
- 当有服务出现异常时, 直接进行失败回滚, 服务降级处理
- 当服务繁忙时, 如果服务出现异常, 不是粗暴的直接报错, 而是返回一个友好的提示, 虽然拒绝了用户的访问, 但是会返回一个结果。
- 服务降级是指系统特别繁忙时, 一些次要服务暂时中断, 优先保证主要服务的畅通, 一切资源优先让给主要服务来使用。

# 引入依赖
在服务消费者中引入Hystrix依赖: 
```xml
<dependency>
	<groupId>org.springframework.cloud</groupId>
	<artifactId>spring-cloud-starter-netflix-hystrix</artifactId>
</dependency>
```

# 开启熔断
```java
@SpringBootApplication
@EnableDiscoveryClient
@EnableHystrix // 开启Hystrix
public class UserConsumerDemoApplication {
	public static void main(String[] args) {
		SpringApplication.run(UserConsumerDemoApplication.class, args);
	}
}
```

# 设置熔断处理函数
```java
@Component
public class UserDao {
	@Autowired
	private RestTemplate restTemplate;

	// 当queryUserById执行超时, 就会执行fallback函数, 返回错误提示
	@HystrixCommand(fallbackMethod = "queryUserByIdFallback")
	public User queryUserById(Long id){
		String url = "http://user-service/user/" + id;
		User user = this.restTemplate.getForObject(url, User.class);
		return user;
	}

	public User queryUserByIdFallback(Long id){
		User user = new User();
		user.setId(id);
		user.setName("用户信息查询出现异常！");
		return user;
	}
}
```