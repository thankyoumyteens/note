# 开启负载均衡

因为Eureka中已经集成了Ribbon, 所以无需引入新的依赖 
```java
@Bean
// 开启负载均衡
@LoadBalanced
public RestTemplate restTemplate() {
	return new RestTemplate(new OkHttp3ClientHttpRequestFactory());
}
```
修改调用方式, 不再手动获取ip和端口, 而是直接通过服务名称调用: 
```java
@Service
public class UserService {
	@Autowired
	private RestTemplate restTemplate;
	@Autowired
	private DiscoveryClient discoveryClient;

	public User queryUserById(Long id) {
		// 地址直接写服务名称即可
		String baseUrl = "http://user-service/user/";
		return this.restTemplate.getForObject(baseUrl + id, User.class));
	}
}
```
