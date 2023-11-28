# FeignClient避免开发调试时服务乱跳

一般在开发环境, 多人同时开发时很多人的服务都注册到同一个注册中心, 自己新增的方法有时无法调用, 如何解决呢？

可以使用指定固定URL为本机的方式, 这样本地代码可以提交, 生产上不用配置即可

```conf
# 开发环境
express.debug.url=http://localhost:8080
# 生产环境不指定URL即可
express.debug.url=
```

```java
@FeignClient(value = "express-service",url = "${express.debug.url}")
public interface ExpressFeign {
}
```
