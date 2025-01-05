# 路由配置

Zuul 会创建对应的路由规则, 也可以在配置文件中手动指定, 格式: `zuul.routes.<serviceId>=<路径表达式>`。

1. 修改 application.yml

```yaml
zuul:
  routes:
    # 服务名: 路径表达式
    eureka-client-demo: /service1/**
```

2. 服务启动后, 访问 http://localhost:27440/service1/service/list, 该请求将最终被路由到 eureka-client-demo 的 /service/list 接口上
