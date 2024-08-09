# 线程隔离

Hystrix 会为每一个 HystrixCommand 创建一个独立的线程池，这样就算某个在 HystrixCommand 包装下的依赖服务出现延迟过高的情况，也只是对该依赖服务的调用产生影响，而不会拖慢其他的服务。

Hystrix 框架会自动为设置了 `@HystrixCommand` 注解的方法实现线程隔离。
