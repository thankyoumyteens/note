# Spring Boot 启动失败 SOP：端口冲突导致容器初始化异常

## 一、问题现象

Spring Boot 应用启动时抛出 `BeanCreationNotAllowedException`，提示 `sqlSessionFactory` 无法在容器销毁期间创建：

```
org.springframework.beans.factory.BeanCreationNotAllowedException: Error creating bean with name ‘sqlSessionFactory’:
Singleton bean creation not allowed while singletons of this factory are in destruction
```

完整日志如下:

```
2026-05-28 14:39:37.310 - [] - [main] WARN  org.springframework.boot.web.servlet.context.AnnotationConfigServletWebServerApplicationContext.()- Exception encountered during context initialization - cancelling refresh attempt: org.springframework.beans.factory.BeanCreationException: Error creating bean with name ’xxlJobExecutor‘ defined in class path resource [cn/hsa/pw/config/XxlJobConfig.class]: Invocation of init method failed; nested exception is com.xxl.rpc.util.XxlRpcException: xxl-rpc provider port[9999] is used. - []
2026-05-28 14:39:37.322 - [] - [main] INFO  org.springframework.context.annotation.AnnotationConfigApplicationContext.()- Closing FeignContext-ant-hsa-iep-msc-nation: startup date [Thu May 28 14:39:16 CST 2026]; parent: org.springframework.boot.web.servlet.context.AnnotationConfigServletWebServerApplicationContext@62360a68 - []
2026-05-28 14:39:37.323 - [] - [main] WARN  org.springframework.context.annotation.AnnotationConfigApplicationContext.()- Exception thrown from ApplicationListener handling ContextClosedEvent - []
org.springframework.beans.factory.BeanCreationNotAllowedException: Error creating bean with name ’sqlSessionFactory‘: Singleton bean creation not allowed while singletons of this factory are in destruction (Do not request a bean from a BeanFactory in a destroy method implementation!)
        at org.springframework.beans.factory.support.DefaultSingletonBeanRegistry.getSingleton(DefaultSingletonBeanRegistry.java:208) ~[spring-beans-5.0.13.RELEASE.jar!/:5.0.13.RELEASE]
        at org.springframework.beans.factory.support.AbstractBeanFactory.doGetBean(AbstractBeanFactory.java:315) ~[spring-beans-5.0.13.RELEASE.jar!/:5.0.13.RELEASE]
        at org.springframework.beans.factory.support.AbstractBeanFactory.getBean(AbstractBeanFactory.java:204) ~[spring-beans-5.0.13.RELEASE.jar!/:5.0.13.RELEASE]
        at org.springframework.context.event.AbstractApplicationEventMulticaster.retrieveApplicationListeners(AbstractApplicationEventMulticaster.java:239) ~[spring-context-5.0.13.RELEASE.jar!/:5.0.13.RELEASE]
        at org.springframework.context.event.AbstractApplicationEventMulticaster.getApplicationListeners(AbstractApplicationEventMulticaster.java:196) ~[spring-context-5.0.13.RELEASE.jar!/:5.0.13.RELEASE]
        at org.springframework.context.event.SimpleApplicationEventMulticaster.multicastEvent(SimpleApplicationEventMulticaster.java:133) ~[spring-context-5.0.13.RELEASE.jar!/:5.0.13.RELEASE]
        at org.springframework.context.support.AbstractApplicationContext.publishEvent(AbstractApplicationContext.java:404) ~[spring-context-5.0.13.RELEASE.jar!/:5.0.13.RELEASE]
        at org.springframework.context.support.AbstractApplicationContext.publishEvent(AbstractApplicationContext.java:410) ~[spring-context-5.0.13.RELEASE.jar!/:5.0.13.RELEASE]
        at org.springframework.context.support.AbstractApplicationContext.publishEvent(AbstractApplicationContext.java:358) ~[spring-context-5.0.13.RELEASE.jar!/:5.0.13.RELEASE]
        at org.springframework.context.support.AbstractApplicationContext.doClose(AbstractApplicationContext.java:1013) ~[spring-context-5.0.13.RELEASE.jar!/:5.0.13.RELEASE]
        at org.springframework.context.support.AbstractApplicationContext.close(AbstractApplicationContext.java:979) ~[spring-context-5.0.13.RELEASE.jar!/:5.0.13.RELEASE]
        at org.springframework.cloud.context.named.NamedContextFactory.destroy(NamedContextFactory.java:76) ~[spring-cloud-context-2.0.4.RELEASE.jar!/:2.0.4.RELEASE]
        at org.springframework.beans.factory.support.DisposableBeanAdapter.destroy(DisposableBeanAdapter.java:256) ~[spring-beans-5.0.13.RELEASE.jar!/:5.0.13.RELEASE]
        at org.springframework.beans.factory.support.DefaultSingletonBeanRegistry.destroyBean(DefaultSingletonBeanRegistry.java:571) ~[spring-beans-5.0.13.RELEASE.jar!/:5.0.13.RELEASE]
        at org.springframework.beans.factory.support.DefaultSingletonBeanRegistry.destroySingleton(DefaultSingletonBeanRegistry.java:543) ~[spring-beans-5.0.13.RELEASE.jar!/:5.0.13.RELEASE]
        at org.springframework.beans.factory.support.DefaultListableBeanFactory.destroySingleton(DefaultListableBeanFactory.java:957) ~[spring-beans-5.0.13.RELEASE.jar!/:5.0.13.RELEASE]
        at org.springframework.beans.factory.support.DefaultSingletonBeanRegistry.destroySingletons(DefaultSingletonBeanRegistry.java:504) ~[spring-beans-5.0.13.RELEASE.jar!/:5.0.13.RELEASE]
        at org.springframework.beans.factory.support.DefaultListableBeanFactory.destroySingletons(DefaultListableBeanFactory.java:964) ~[spring-beans-5.0.13.RELEASE.jar!/:5.0.13.RELEASE]
        at org.springframework.context.support.AbstractApplicationContext.destroyBeans(AbstractApplicationContext.java:1061) ~[spring-context-5.0.13.RELEASE.jar!/:5.0.13.RELEASE]
        at org.springframework.context.support.AbstractApplicationContext.refresh(AbstractApplicationContext.java:564) ~[spring-context-5.0.13.RELEASE.jar!/:5.0.13.RELEASE]
        at org.springframework.boot.web.servlet.context.ServletWebServerApplicationContext.refresh(ServletWebServerApplicationContext.java:142) ~[spring-boot-2.0.9.RELEASE.jar!/:2.0.9.RELEASE]
        at org.springframework.boot.SpringApplication.refresh(SpringApplication.java:754) ~[spring-boot-2.0.9.RELEASE.jar!/:2.0.9.RELEASE]
        at org.springframework.boot.SpringApplication.refreshContext(SpringApplication.java:386) ~[spring-boot-2.0.9.RELEASE.jar!/:2.0.9.RELEASE]
        at org.springframework.boot.SpringApplication.run(SpringApplication.java:307) ~[spring-boot-2.0.9.RELEASE.jar!/:2.0.9.RELEASE]
        at org.springframework.boot.SpringApplication.run(SpringApplication.java:1242) ~[spring-boot-2.0.9.RELEASE.jar!/:2.0.9.RELEASE]
        at org.springframework.boot.SpringApplication.run(SpringApplication.java:1230) ~[spring-boot-2.0.9.RELEASE.jar!/:2.0.9.RELEASE]
        at cn.hsa.pw.ExampleApplication.main(ExampleApplication.java:38) ~[classes!/:?]
        at sun.reflect.NativeMethodAccessorImpl.invoke0(Native Method) ~[?:1.8.0_422]
        at sun.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:62) ~[?:1.8.0_422]
        at sun.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43) ~[?:1.8.0_422]
        at java.lang.reflect.Method.invoke(Method.java:498) ~[?:1.8.0_422]
        at org.springframework.boot.loader.MainMethodRunner.run(MainMethodRunner.java:48) ~[application.jar:?]
        at org.springframework.boot.loader.Launcher.launch(Launcher.java:87) ~[application.jar:?]
        at org.springframework.boot.loader.Launcher.launch(Launcher.java:50) ~[application.jar:?]
        at org.springframework.boot.loader.JarLauncher.main(JarLauncher.java:51) ~[application.jar:?]
```

—

## 二、根因分析

| 层级 | 异常 | 性质 |
|—|—|—|
| **根因** | `XxlRpcException: xxl-rpc provider port[9999] is used.` | 端口 9999 被占用，XXL-Job executor 初始化失败 |
| 级联 | `BeanCreationException: Error creating bean with name ‘xxlJobExecutor’` | Bean 创建失败，Spring 取消上下文刷新 |
| 连带 | `BeanCreationNotAllowedException: ... sqlSessionFactory ...` | 容器销毁期间，某个 `ContextClosedEvent` 监听器尝试获取已销毁的 Bean，属于清理过程中的二次异常 |

**关键判断依据**：堆栈中 `AbstractApplicationContext.refresh()` 在第 564 行进入 `destroyBeans()`，说明 `refresh()` 内部已在此之前捕获到其他异常，被迫进入清理流程。`BeanCreationNotAllowedException` 永远不是第一现场。

—

## 三、排查思路

```
启动失败
  │
  └─→ 1. 看第一条 WARN/ERROR（不是最后一条）
        │  日志中第一个异常才是根因，后面的通常是清理过程的连带错误
        │
        └─→ 2. 定位根因异常类型
              │
              ├─ XxlRpcException / port is used → 端口冲突
              ├─ Connection refused / timeout    → 数据库/中间件不可达
              ├─ ClassNotFoundException         → 依赖缺失
              └─ ...                            → 根据具体异常处理
                    │
                    └─→ 3. 验证端口占用情况
                          ss -tlnp | grep <端口>
                          lsof -i :<端口>
                          netstat -anp | grep <端口>
```

—

## 四、解决方案

**第一步**：找到 XXL-Job 端口配置位置。

```bash
grep -r “9999” . 2>/dev/null
grep -r “xxl” . 2>/dev/null | grep -i port
```

**第二步**：修改配置，更换为未占用的端口。

```yaml
# application.yml 或对应配置文件
xxl:
  job:
    executor:
      port: 9998 # 换一个未被占用的端口
```

**第三步**：重新打包部署，验证启动成功。

—

## 五、通用故障排查口诀

> **第一个异常是根因，最后一个往往是误导。**  
> 启动失败的日志从第一条 WARN/ERROR 读起，不要从堆栈底部往上读。
