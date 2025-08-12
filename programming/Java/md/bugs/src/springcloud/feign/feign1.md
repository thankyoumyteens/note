# Consider defining a bean of type

报错：Consider defining a bean of type ‘com.itmayiedu.feign.MemberApiFeign’ in your configuration.

## 原因

1. 没有在启动项上添加注解 @EnableFeignClients
2. 启动项的包结构问题, 导致 FeignClient 没有被 spring 扫描到
