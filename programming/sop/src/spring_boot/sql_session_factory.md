# Spring Boot 启动报 `sqlSessionFactory` 销毁异常：排查 XXL-Job 端口冲突

> 适用场景：Spring Boot 启动过程中出现 `BeanCreationNotAllowedException`，同时日志中存在端口占用、Bean 初始化失败或上下文刷新失败。

## 一、问题现象

应用启动失败，日志末尾出现：

```text
org.springframework.beans.factory.BeanCreationNotAllowedException:
Error creating bean with name 'sqlSessionFactory':
Singleton bean creation not allowed while singletons of this factory are in destruction
```

但在该异常之前，日志已经出现真正触发启动失败的异常：

```text
BeanCreationException: Error creating bean with name 'xxlJobExecutor'
Caused by: com.xxl.rpc.util.XxlRpcException:
xxl-rpc provider port[9999] is used.
```

## 二、根因分析

| 层级         | 异常                                                   | 含义                                          |
| ------------ | ------------------------------------------------------ | --------------------------------------------- |
| 根因         | `XxlRpcException: xxl-rpc provider port[9999] is used` | XXL-Job executor 监听端口被占用，初始化失败   |
| 级联异常     | `BeanCreationException: xxlJobExecutor`                | Bean 创建失败，Spring 取消上下文刷新          |
| 清理阶段异常 | `BeanCreationNotAllowedException: sqlSessionFactory`   | 容器销毁期间，监听器又尝试获取正在销毁的 Bean |

本案例中，`sqlSessionFactory` 异常发生在 Spring 清理失败上下文的过程中，不是导致本次启动失败的第一现场。

> 不要机械地把“第一条 WARN/ERROR”当作根因。应从上下文初始化失败的首个异常链开始，沿 `Caused by` 追到最内层，再结合此前日志确认触发点。

## 三、排查流程

### Step 1：定位首次上下文初始化失败

从启动日志中搜索以下关键字：

```bash
grep -nE "Application run failed|Exception encountered during context initialization|BeanCreationException|Caused by:" <application.log>
```

重点查看：

1. Spring 开始关闭上下文之前出现的异常。
2. 完整的 `Caused by` 链。
3. 失败 Bean 的初始化方法及其依赖资源。

### Step 2：确认端口是否正在监听

在应用实际运行的宿主机或对应网络命名空间内执行：

```bash
PORT=9999
sudo ss -ltnp "sport = :${PORT}"
```

如果当前环境的 `ss` 不支持过滤表达式，可使用：

```bash
sudo ss -ltnp | grep -E ":9999([[:space:]]|$)"
sudo lsof -nP -iTCP:9999 -sTCP:LISTEN
```

记录占用进程的 PID、启动命令、所属容器或服务，不要在确认身份前终止进程。

### Step 3：确认端口配置来源

在应用源码或部署配置目录执行：

```bash
grep -RIn --exclude-dir=.git "9999" .
grep -RIn --exclude-dir=.git -E "xxl.*port|executor.*port" .
```

同时检查环境变量、配置中心、启动参数和 Kubernetes manifest，避免只修改仓库内配置却被外部配置覆盖。

### Step 4：选择处置方式

根据端口占用者选择：

| 场景                             | 处置方式                                               |
| -------------------------------- | ------------------------------------------------------ |
| 合法运行实例正在使用端口         | 不终止对方；调整当前实例端口或调度位置                 |
| 同一应用的旧实例或残留容器       | 通过部署平台正常下线并清理旧实例                       |
| 误启动的本机进程                 | 确认业务影响后优先发送 `SIGTERM`，必要时再升级处理     |
| 多副本被配置为争用同一宿主机端口 | 调整网络、端口或调度策略，不能只在单次部署中临时换端口 |

如果决定修改 XXL-Job executor 端口，必须同步检查服务发现、调度中心、容器端口、`hostPort`、防火墙和健康检查等依赖配置。

示例配置仅用于说明配置位置，端口值应根据实际环境确定：

```yaml
xxl:
  job:
    executor:
      port: 9998
```

## 四、验证

重新部署后至少验证：

1. 新端口处于监听状态，且 PID/容器身份正确。
2. 日志中不再出现 `port is used` 和上下文初始化失败。
3. 应用健康检查通过。
4. XXL-Job executor 已使用正确地址和端口完成注册。
5. 调度一次低风险测试任务，确认回调链路正常。

## 五、排查要点

> 从“上下文为何开始销毁”向前追，而不是只处理销毁阶段最后打印的异常。

`BeanCreationNotAllowedException` 可能是重要问题，但在启动失败场景中，应先确认它是否只是清理阶段的连带异常。
