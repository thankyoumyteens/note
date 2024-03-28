# 调度中心部署

## 配置文件

调度服务器(powerjob-server)为了支持环境隔离, 分别采用了日常(application-daily.properties)、预发(application-pre.properties)和线上(application-product.properties)三套配置文件

| 配置项                            | 含义                               | 可选                              |
|--------------------------------|----------------------------------|---------------------------------|
| `server.port`                    | SpringBoot配置, HTTP端口号, 默认7700      | 否, 且不建议更改                        |
| `oms.akka.port`                  | PowerJob配置, Akka端口号, 默认10086       | 否, 且不建议更改                        |
| `oms.http.port`                  | PowerJob配置, 多语言客户端HTTP端口号, 默认10010 | 否, 且不建议更改                        |
| `oms.table-prefix`               | 自定义数据库表名前缀                       | 是                               |
| `spring.datasource.core.xxx`     | 关系型数据库连接配置                       | 否                               |
| `spring.mail.xxx`                | 邮件配置                             | 是, 未配置情况下将无法使用邮件报警功能             |
| `spring.data.mongodb.xxx`        | MongoDB连接配置                      | 是, 未配置情况下将无法在集群模式下保证容器和在线日志的高可用性 |
| `oms.container.retention.local`  | 本地容器保留天数, 负数代表永久保留                | 是                               |
| `oms.container.retention.remote` | 远程容器保留天数, 负数代表永久保留                | 是                               |
| `oms.instanceinfo.retention`     | 任务实例和工作流实例信息的保留天数, 负数代表永久保留(不建议)  | 是, 推荐使用默认配置, 生产环境保留7天             |

## 源码部署

1. 克隆: `git clone https://github.com/PowerJob/PowerJob.git`, 下载本项目源码。
2. 修改对应环境的配置文件(application-xxx.properties)。
3. 打包: `mvn clean package -U -Pdev -DskipTests`, 构建调度服务器(powerjob-server)Jar 文件。
4. 运行: `java -jar xxx.jar --spring.profiles.active=product`, 指定生效的配置文件。注意, 宿主机需要打开 7700(HTTP 服务)和 10086(AKKA 服务)端口。

## 部署前端页面(powerjob-console)

1. 源码克隆: `git clone https://github.com/PowerJob/PowerJob-Console.git`
1. 替换地址: 修改`.env.product` 中的 `VUE_APP_BASE_URL` 为调度服务器地址
1. `npm install && npm run build`
1. 将构建结果 dist 文件夹拷入 Nginx 静态目录下, 修改配置文件, 重启 nginx

# SpringBoot 应用接入

```xml
<dependency>
    <groupId>tech.powerjob</groupId>
    <artifactId>powerjob-worker-spring-boot-starter</artifactId>
    <version>${latest.powerjob.version}</version>
</dependency>
```

```conf
# akka 工作端口, 可选, 默认 27777
powerjob.worker.akka-port=27777
# 接入应用名称, 用于分组隔离, 推荐填写 本 Java 项目名称
powerjob.worker.app-name=my-powerjob-worker
# 调度服务器地址, IP:Port 或 域名, 多值逗号分隔
powerjob.worker.server-address=127.0.0.1:7700,127.0.0.1:7701
# 持久化方式, 可选, 默认 disk
powerjob.worker.store-strategy=disk
# 任务返回结果信息的最大长度, 超过这个长度的信息会被截断, 默认值 8192
powerjob.worker.max-result-length=4096
# 单个任务追加的工作流上下文最大长度, 超过这个长度的会被直接丢弃, 默认值 8192
powerjob.worker.max-appended-wf-context-length=4096
```

## 编写自己的处理器

```java
@Slf4j
@Component
public class StandaloneProcessorDemo implements BasicProcessor {
    @Override
    public ProcessResult process(TaskContext context) throws Exception {
        // PowerJob 在线日志功能, 使用该 Logger 打印的日志可以直接在 PowerJob 控制台查看
        OmsLogger omsLogger = context.getOmsLogger();
        omsLogger.info("StandaloneProcessorDemo start process,context is {}.", context);
        return new ProcessResult(true, "process successfully~");
    }
}
```
