# 使用服务实现可选的依赖

使用者可以从服务提供者模块中获得零个或多个服务类型的实现。获取零个或一个服务实现只是这种通用机制的一个特例。

```java
FastJson fastJson = ServiceLoader.load(FastJson.class)
                                 .findFirst()
                                 .orElse(myFallBack());
```
