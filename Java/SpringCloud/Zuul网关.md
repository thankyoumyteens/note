# Zuul网关
服务网关是微服务架构中一个不可或缺的部分。通过服务网关统一向外系统提供REST API的过程中, 除了具备服务路由、均衡负载功能之外, 它还具备了权限控制等功能。

不管是来自于客户端(PC或移动端)的请求, 还是服务内部调用。一切对服务的请求都会经过Zuul这个网关, 然后再由网关来实现 鉴权、动态路由等等操作。Zuul就是我们服务的统一入口。

# 网关
添加Zuul依赖
```xml
<dependency>
	<groupId>org.springframework.cloud</groupId>
	<artifactId>spring-cloud-starter-zuul</artifactId>
</dependency>
```
启动类
```java
@SpringBootApplication
@EnableZuulProxy // 开启Zuul的网关功能
public class ZuulDemoApplication {
	public static void main(String[] args) {
		SpringApplication.run(ZuulDemoApplication.class, args);
	}
}
```
配置
```yaml
server:
  port: 10010 #服务端口
spring: 
  application:  
    name: api-gateway #指定服务名
```
路由规则
```yaml
zuul:
  routes:
    user-service: # 这里是路由id, 随意写
      path: /user-service/** # 这里是映射路径
      url: http://127.0.0.1:8081 # 映射路径对应的实际url地址
```

# zuul+eureka
添加Eureka客户端依赖
```xml
<dependency>
	<groupId>org.springframework.cloud</groupId>
	<artifactId>spring-cloud-starter-netflix-eureka-client</artifactId>
</dependency>
```
开启Eureka客户端发现功能
```java
@SpringBootApplication
@EnableZuulProxy // 开启Zuul的网关功能
@EnableDiscoveryClient // 开启Eureka客户端
public class ZuulDemoApplication {
	public static void main(String[] args) {
		SpringApplication.run(ZuulDemoApplication.class, args);
	}
}
```
添加Eureka配置
```yaml
eureka:
	client:
		# 获取服务列表的周期: 5s
    registry-fetch-interval-seconds: 5
    service-url:
      defaultZone: http://127.0.0.1:10086/eureka
  instance:
    prefer-ip-address: true
    ip-address: 127.0.0.1
```
修改路由配置
```yaml
zuul:
  routes:
    user-service: # 这里是路由id, 随意写
      path: /user-service/** # 这里是映射路径
      serviceId: user-service # 指定服务名称
```
上面关于user-service的配置可以简化为一条
```yaml
zuul:
	routes:
		# 路由id和映射路径相同
    user-service: /user-service/** # 这里是映射路径
```
- 默认情况下, 一切服务的映射路径就是服务名本身。
- 例如服务名为user-service, 则默认的映射路径就是/user-service/**
- 也就是说, 刚才的路由规则完全不用配置

路由前缀
```yaml
zuul:
  prefix: /api # 添加路由前缀
  routes:
      user-service: # 这里是路由id, 随意写
        path: /user-service/** # 这里是映射路径
        service-id: user-service # 指定服务名称
```

# 过滤器
正常流程: 
- 请求到达首先会经过pre类型过滤器, 而后到达routing类型, 进行路由, 请求就到达真正的服务提供者, 执行请求, 返回结果后, 会到达post过滤器。而后返回响应。

异常流程: 
- 整个过程中, pre或者routing过滤器出现异常, 都会直接进入error过滤器, 再error处理完毕后, 会将请求交给POST过滤器, 最后返回给用户。
- 如果是error过滤器自己出现异常, 最终也会进入POST过滤器, 而后返回。
- 如果是POST过滤器出现异常, 会跳转到error过滤器, 但是与pre和routing不同的时, 请求不会再到达POST过滤器了。

## 自定义过滤器
```java
@Component
public class LoginFilter extends ZuulFilter{
	// 返回过滤器的类型
	@Override
	public String filterType() {
		// pre: 请求在被路由之前执行
		// routing: 在路由请求时调用
		// post: 在routing和errror过滤器之后调用
		// error: 处理请求时发生错误调用
		return "pre";
	}
	
	// 定义过滤器的执行顺序, 数字越小优先级越高
	@Override
	public int filterOrder() {
		return 1;
	}

	@Override
	public boolean shouldFilter() {
		// 返回true, 代表过滤器生效。
		return true;
	}

	// 过滤器的具体业务逻辑
	@Override
	public Object run() throws ZuulException {
		// 登录校验逻辑。
		RequestContext ctx = RequestContext.getCurrentContext();
		HttpServletRequest req = ctx.getRequest();
		String token = req.getParameter("access-token");
		if(token == null || "".equals(token.trim())){
			// 没有token, 登录校验失败, 拦截
			ctx.setSendZuulResponse(false);
			ctx.setResponseStatusCode(HttpStatus.UNAUTHORIZED.value());
		}
		// 校验通过, 可以考虑把用户信息放入上下文, 继续向后执行
		return null;
	}
}
```

# 负载均衡和熔断
Zuul中默认就已经集成了Ribbon负载均衡和Hystrix熔断机制。但是所有的超时策略都是走的默认值, 比如熔断超时时间只有1S, 很容易就触发了。因此建议手动进行配置: 
```yaml
zuul:
  retryable: true
ribbon:
  ConnectTimeout: 250 # 连接超时时间(ms)
  ReadTimeout: 2000 # 通信超时时间(ms)
  OkToRetryOnAllOperations: true # 是否对所有操作重试
  MaxAutoRetriesNextServer: 2 # 同一服务不同实例的重试次数
  MaxAutoRetries: 1 # 同一实例的重试次数
hystrix:
  command:
  	default:
        execution:
          isolation:
            thread:
              timeoutInMillisecond: 6000 # 熔断超时时长: 6000ms
```
