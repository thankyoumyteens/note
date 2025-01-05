# JVM 统一日志框架

JVM 统一日志框架为 JVM 的所有组件提供了一个通用的日志记录系统。垃圾回收的日志也改用这个新框架了。

使用 JVM 参数 `-Xlog` 打印日志。格式:

```sh
-Xlog[:[what][:[output][:[decorators][:output-options[,...]]]]]
```

- what: 指定 tag 和 level 的组合, 用来控制日志输出哪些内容
- output: 日志输出到哪里
- decorators: 日志格式
- output-options: 日志的其它设置

## Tag 和 Level

每条日志消息都会关联一个 level 和一个 tag。 level 控制日志的详情, tag 控制的是日志包含什么内容或者涉及到哪个 JVM 组件(比如, gc, jit, 或者 os)。

### level 的可选值

- off
- trace
- debug
- info
- warning
- error

### tag 的可选值

tag 的可选值有很多, 可以使用 `-Xlog:help` 查看全部。可以指定 `all` 来输出所有组件的日志。

### tag 和 level 组合的格式

```sh
tag=level
```

比如: `-Xlog:gc=info`, 表示只输出 gc 组件的 info 级别日志。 `-Xlog:all=info`, 表示输出所有组件的 info 级别日志。

## Output

output 的可选值:

- `stdout`: 日志输出到标准输出
- `stderr`: 日志输出到标准错误输出
- `file=文件路径`: 日志输出到指定文件

日志输出到文件时, 可以在文件名中使用 `%p` 和 `%t` 分别自动替换成 JVM 的 PID 和开始时间。

## Decorations

Decorations 会在日志消息前面输出, 比如：

```sh
[6.567s][info][gc,old] Old collection complete
```

其中 `[6.567s][info][gc,old]` 就是 Decorations。

decorators 的可选值如下:

- `time` 或者 `t`: 当前时间, ISO-8601 格式
- `utctime` 或者 `utc`: 协调世界时
- `uptime` 或者 `u`: 从 JVM 启动开始到打印日志为止的时间。比如, 6.567s
- `timemillis` 或者 `tm`: 相当于使用 System.currentTimeMillis() 获取的时间
- `uptimemillis` 或者 `um`: 从 JVM 启动开始到打印日志为止的毫秒数
- `timenanos` 或者 `tn`: 相当于使用 System.nanoTime() 获取的时间
- `uptimenanos` 或者 `un`: 从 JVM 启动开始到打印日志为止的纳秒数
- `hostname` 或者 `hn`: 主机名
- `pid` 或者 `p`: 进程标识符
- `tid` 或者 `ti`: 线程标识符
- `level` 或者 `l`: 日志的 level
- `tags` 或者 `tg`: 日志的 tag
- `none`: 不输出任何 Decorations

使用示例:

```sh
-Xlog:all=info:stdout:t,utc,u,tm,um,tn,un,hn,p,ti,l,tg
-Xlog:all=info:stdout:none
```

## GC 日志输出

| 旧版 JVM 参数                      | 使用 Xlog 替换                | 说明                                                          |
| ---------------------------------- | ----------------------------- | ------------------------------------------------------------- |
| G1PrintHeapRegions                 | `-Xlog:gc+region=trace`       | 无                                                            |
| GCLogFileSize                      | 无                            | 这个设置改为由日志框架处理                                    |
| NumberOfGCLogFiles                 | 无                            | 这个设置改为由日志框架处理                                    |
| PrintAdaptiveSizePolicy            | `-Xlog:gc+ergo*=日志级别`     | 日志级别使用 debug 或者 trace 替代 PrintAdaptiveSizePolicy    |
| PrintGC                            | `-Xlog:gc`                    | 无                                                            |
| PrintGCApplicationConcurrentTime   | `-Xlog:safepoint`             | 会和下面的配置一起打印                                        |
| PrintGCApplicationStoppedTime      | `-Xlog:safepoint`             | 会和上面的配置一起打印                                        |
| PrintGCCause                       | 无                            | GC cause 现在总是会打印                                       |
| PrintGCDateStamps                  | 无                            | 这个设置改为由日志框架处理                                    |
| PrintGCDetails                     | `-Xlog:gc*`                   | 无                                                            |
| PrintGCID                          | 无                            | GC ID 现在总是会打印                                          |
| PrintGCTaskTimeStamps              | `-Xlog:gc+task*=debug`        | 无                                                            |
| PrintGCTimeStamps                  | 无                            | 这个设置改为由日志框架处理                                    |
| PrintHeapAtGC                      | `-Xlog:gc+heap=trace`         | 无                                                            |
| PrintReferenceGC                   | `-Xlog:gc+ref*=debug`         | 在旧版中, 只有开启了 PrintGCDetails, 这个设置才会生效         |
| PrintStringDeduplicationStatistics | `-Xlog:gc+stringdedup*=debug` | 无                                                            |
| PrintTenuringDistribution          | `-Xlog:gc+age*=日志级别`      | 日志级别使用 debug 或者 trace 替代 PrintTenuringDistribution. |
| UseGCLogFileRotation               | 无                            | 为 PrintTenuringDistribution 记录的日志                       |

## 运行时日志输出

| 旧版 JVM 参数             | 使用 Xlog 替换                            | 说明                                             |
| ------------------------- | ----------------------------------------- | ------------------------------------------------ |
| TraceExceptions           | `-Xlog:exceptions=info`                   | 无                                               |
| TraceClassLoading         | `-Xlog:class+load=日志级别`               | 使用 info 打印常规信息, 使用 debug 打印附加信息  |
| TraceClassLoadingPreorder | `-Xlog:class+preorder=debug`              | 无                                               |
| TraceClassUnloading       | `-Xlog:class+unload=日志级别`             | 使用 info 打印常规信息, 使用 debug 打印附加信息  |
| `-verbose:class`          | `-Xlog:class+load=info,class+unload=info` | 无                                               |
| VerboseVerification       | `-Xlog:verification=info`                 | 无                                               |
| TraceClassPaths           | `-Xlog:class+path=info`                   | 无                                               |
| TraceClassResolution      | `-Xlog:class+resolve=debug`               | 无                                               |
| TraceClassInitialization  | `-Xlog:class+init=info`                   | 无                                               |
| TraceLoaderConstraints    | `-Xlog:class+loader+constraints=info`     | 无                                               |
| TraceClassLoaderData      | `-Xlog:class+loader+data=日志级别`        | 使用 debug 打印常规信息, 使用 trace 打印附加信息 |
| TraceSafepointCleanupTime | `-Xlog:safepoint+cleanup=info`            | 无                                               |
| TraceSafepoint            | `-Xlog:safepoint=debug`                   | 无                                               |
| TraceMonitorInflation     | `-Xlog:monitorinflation=debug`            | 无                                               |
| TraceBiasedLocking        | `-Xlog:biasedlocking=日志级别`            | 使用 info 打印常规信息, 使用 trace 打印附加信息  |
| TraceRedefineClasses      | `-Xlog:redefine+class*=日志级别`          | 无                                               |

## 常用示例

- `-Xlog`: 相当于 `-Xlog:all=info:stdout:uptime,levels,tags`
- `-Xlog:gc`: 在控制台打印 info 级别的 gc 日志
- `-Xlog:gc,safepoint`: 在控制台打印 info 级别的 gc 和 safepoint 日志
- `-Xlog:gc+ref=debug`: 在控制台打印 debug 级别的 gc 和 ref 日志
- `-Xlog:gc=debug:file=gc.txt:none`: 在 gc.txt 文件中打印 debug 级别的 gc 日志, 不使用 Decorations
- `-Xlog:gc=trace:file=gctrace.txt:uptimemillis,pid:filecount=5,filesize=1024`: 在 gctrace.txt 文件中打印 trace 级别的 gc 日志, Decorations 使用 uptimemillis 和 pid, 系统会维护最多 5 个日志文件, 每个文件的大小上限是 1 MB。当最新的日志文件达到 1 MB 时, 它会被关闭, 并且一个新的空日志文件会被创建, 同时最老的那个日志文件如果存在的话将被删除或归档, 以保持总共有 5 个日志文件: gctrace.txt.0, gctrace.txt.1, gctrace.txt.2, gctrace.txt.3, gctrace.txt.4
- `-Xlog:gc::uptime,tid`: 在控制台打印 info 级别的 gc 日志, Decorations 使用 uptime 和 tid
- `-Xlog:gc*=info,safepoint*=off`: 在控制台打印 info 级别的和 gc 有关的日志, 不打印和 safepoint 有关的日志
- `-Xlog:disable -Xlog:safepoint=trace:safepointtrace.txt`: 关闭日志(禁用所有的默认日志设置), 然后在 safepointtrace.txt 中打印 trace 级别的 safepoint 日志
