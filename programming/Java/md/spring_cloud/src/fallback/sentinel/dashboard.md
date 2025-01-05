# Sentinel 控制台

```sh
# 下载
wget https://github.com/alibaba/Sentinel/releases/download/1.8.8/sentinel-dashboard-1.8.8.jar
# 运行
java -Dserver.port=8081 -Dcsp.sentinel.dashboard.server=localhost:8081 -Dproject.name=sentinel-dashboard -jar sentinel-dashboard-1.8.8.jar
```

启动后访问 http://localhost:8081 进入 Sentinel 控制台, 默认的用户名和密码：sentinel/sentinel。

## 修改密码

在执行 jar 命令时指定参数设置:

```sh
-Dsentinel.dashboard.auth.username=用户名
-Dsentinel.dashboard.auth.password=密码
```

## 微服务接入控制台

1. 依赖

```xml
<dependency>
    <groupId>com.alibaba.cloud</groupId>
    <artifactId>spring-cloud-starter-alibaba-sentinel</artifactId>
    <version>2.2.9.RELEASE</version>
</dependency>
```

2. 配置

```yaml
spring:
  cloud:
    sentinel:
      transport:
        # 指定控制台的地址
        dashboard: localhost:8081
      # sentinel是懒加载机制, 只有访问过一次的资源才会被监控
      # 取消控制台懒加载, 项目启动即连接Sentinel
      eager: true
```
