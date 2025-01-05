# 替换默认的 httpclient

Feign 在默认情况下使用的是 JDK 原生的 URLConnection 发送 HTTP 请求, 没有连接池, 但是对每个地址会保持一个长连接, 即利用 HTTP 的 persistence connection。

可以查看 `feign.Client#execute` 方法使用的是哪个实现类, 判断使用的是哪个 http 客户端。

## 替换成 ApacheHttpClient

1. 依赖

```xml
<dependency>
    <groupId>org.apache.httpcomponents</groupId>
    <artifactId>httpclient</artifactId>
</dependency>
<dependency>
    <groupId>io.github.openfeign</groupId>
    <artifactId>feign-httpclient</artifactId>
</dependency>
```

2. 配置

```yaml
feign:
  client:
    httpclient:
      enabled: true
```
