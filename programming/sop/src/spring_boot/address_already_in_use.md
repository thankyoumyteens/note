# K8s Pod 启动报 `Address already in use`：排查节点与容器端口占用

> 适用场景:K8s Pod 内应用启动报 `java.net.BindException: Address already in use` / `Protocol handler start failed`,端口被占用无法启动。
> 本 SOP 基于 2026-07-13 一次真实排查整理(PID 2756882 的孤儿 java 进程占用 hostNetwork 的 8085)。

---

## 一、典型报错

```
Failed to start connector [Connector[HTTP/1.1-8085]]
org.apache.catalina.LifecycleException: Protocol handler start failed
Caused by: java.net.BindException: Address already in use
    at org.apache.tomcat.util.net.NioEndpoint.initServerSocket(NioEndpoint.java:225)
```

**根因**:配置的监听端口(如 8085)已被同网络命名空间内的其他进程占住,K8s 容器环境下常见原因是 **hostNetwork/hostPort 的旧实例或孤儿进程未退出**。

---

## 二、排查思路(总览)

容器内端口冲突的特殊性:

- 同 Pod 多容器**共享 network namespace**,sidecar 可能抢端口;
- `hostNetwork: true` 时,容器直接绑宿主机网卡,**端口是节点级稀缺资源**;
- kubelet PLEG 不健康时,旧 Pod 容器杀不干净,java 进程变**孤儿**继续占端口;
- 容器进程在独立 PID namespace,宿主机 `ss -p` / `lsof` 可能**看不到进程名**。

排查按"从宿主机网络层 → 定位到具体进程 → 确认身份 → 清理"推进。

---

## 二·补、什么是 Sidecar(背景知识)

**Sidecar(边车)** 是借自摩托车的比喻:边车挂在主车旁边,跟着主车走,辅助主车完成任务,但自己不是主车。
在 K8s/微服务里,它指**和业务容器跑在同一个 Pod 里、配套提供辅助功能的另一个容器**。

### 核心特点

同一个 Pod 内的容器:

- **共享 network namespace** → 共享 IP 和端口(这就是 sidecar 会和业务抢端口的根本原因);
- **共享存储卷**;
- 整个 Pod 作为整体被调度和伸缩。

> Pod = 业务容器(主车)+ sidecar 容器(边车),二者是平等的两个容器,只是分工不同。

### 常见 sidecar 类型

| Sidecar                                 | 干什么                                               |
| --------------------------------------- | ---------------------------------------------------- |
| Service Mesh 代理(Istio Envoy、Linkerd) | 拦截所有进出流量,做负载均衡、熔断、加密、可观测性    |
| 日志采集(Filebeat、Fluentd)             | 读业务容器写出的日志文件,转发到日志中心              |
| 监控 agent                              | 采集指标暴露给 Prometheus                            |
| 配置/密钥热加载                         | 监听配置变更,刷新业务配置                            |
| 本地代理/网关(MOSN、tengine 本地代理)   | Pod 内做协议转换、本地路由——**很可能是端口冲突元凶** |

### 排查时的判别

- 有 kubectl 时:

```bash
kubectl get pod <pod-name> -n <ns> -o jsonpath='{.spec.containers[*].name}{"\n"}'
```

输出里除业务容器外若还有 `istio-proxy`、`mesh`、`agent`、`log`、`sidecar` 字样的容器,即 sidecar。

- **sidecar 冲突 vs 孤儿进程冲突**(本 SOP 两种高频场景):

| 类型               | 特征                                                                                            | 解法                          |
| ------------------ | ----------------------------------------------------------------------------------------------- | ----------------------------- |
| sidecar 冲突       | 每次必现、同 Pod 内抢端口、业务容器内 `ss` 能看到 LISTEN 但看不到进程(进程在 sidecar 的 PID ns) | 业务端口避让 sidecar,不可重叠 |
| 孤儿进程冲突(本次) | 偶发、残留老进程、能看到 java 进程身份                                                          | 杀孤儿 + 修节点               |

---

## 二·补2、什么是 kubelet PLEG(背景知识)

**PLEG** = **Pod Lifecycle Event Generator**(Pod 生命周期事件生成器),是 **kubelet 内部的一个核心组件**,负责感知本节点上 Pod/容器的真实状态并驱动 kubelet 做相应处理。

### 工作机制

```
容器运行时(docker/containerd)
        ↓ PLEG 周期性轮询(relist,约每 1s)
   PLEG
        ↓ 对比真实状态 vs 期望状态,产出状态变化事件
   kubelet syncLoop
        ↓ 按事件处理:启动/杀容器/上报状态
```

PLEG 每一轮做两件事:

1. **relist**:向容器运行时(CRI)查询本节点所有 Pod/容器的当前真实状态(running / exited / 不存在……);
2. **对比**:把"真实状态"和 kubelet 内存里的"期望状态"比对,有变化就生成事件(如"容器 X 从 running → exited"),投递给 kubelet 主循环处理。

### 为什么端口排查要懂它

PLEG 出问题 → **kubelet 看不清容器真实状态** → 该杀的容器没杀、该启的没启、状态上报卡住。这正是本次孤儿端口的源头:

- 日志报 `PLEG: Write status` → kubelet 无法把容器真实状态写回;
- 紧跟 `StopPodSandbox` / `KillPodSandbox failed` → kubelet 想停旧沙箱但**对运行时的调用失败**;
- 结果:Pod 在 K8s 视角被删了,但底层容器/进程**没被杀干净**,java 变孤儿继续占 hostNetwork 的 8085。

PLEG 不健康通常由底层容器运行时卡死、僵死进程、cgroup 残留、磁盘 IO 问题等引起。

### 怎么判断 PLEG 是否健康

```bash
# 看是否报 PLEG 错误
sudo journalctl -u kubelet --since "1 hour ago" | grep -i pleg

# 有 kubectl + metrics 时,看 PLEG 延迟
kubectl get --raw '/metrics' | grep kubelet_pleg
```

关注指标:

- `kubelet_pleg_relist_duration_seconds` 高 → relist 卡顿(容器运行时慢);
- `kubelet_pleg_last_seen_seconds` 大 → 很久没产出事件;
- 日志持续刷 `PLEG: Write status` / `PLEG is not healthy` → **明确不健康**。

> k8s 1.26+ 有逐步用 **Evented PLEG**(事件驱动)替代轮询式 PLEG 的趋势,降开销,但排查思路一致——本质都是"kubelet 感知容器真实状态"的机制。
>
> 一句话:**PLEG 是 kubelet 的"容器状态感知雷达",它坏了 → kubelet 删 Pod 时杀不干净容器 → 留下占端口的孤儿进程**。

---

## 三、分步操作

### Step 1 —— 确认被占用端口与状态

在**宿主机**或**报错 Pod 所在容器**内执行。

```bash
# 把端口转换成十六进制
PORT=8085
HEX=$(printf '%04X' $PORT)        # 1F95

# 8085 的十六进制 = 1F95,先在 /proc/net/tcp 找 LISTEN(0A) 记录
cat /proc/net/tcp | grep :1F95
```

输出字段说明(空格分隔):

- 第 2 列 `本地地址:端口`(小端十六进制)
- 第 4 列 `0A` = LISTEN,`06` = TIME_WAIT
- 第 8 列 UID
- 第 10 列 **inode**(全机唯一,下一步反查进程用)

示例:

```
73: 00000000:1F95 00000000:0000 0A ... 0 0 3816011173 ...
```

→ `0.0.0.0:8085` 处于 LISTEN,inode `3816011173`。

### Step 2 —— 看是否有进程信息

```bash
sudo ss -tlnp | grep 8085
sudo netstat -tlnp 2>/dev/null | grep 8085
```

输出示例:

```sh
[root@ant-k8snode-test-9 ~]# sudo ss -tlnp | grep 8085
LISTEN    0         128                 0.0.0.0:8085             0.0.0.0:*       users:(("java",pid=2756882,fd=348))
[root@ant-k8snode-test-9 ~]# sudo netstat -tlnp 2>/dev/null | grep 8085
tcp        0      0 0.0.0.0:8085            0.0.0.0:*               LISTEN      2756882/java
[root@ant-k8snode-test-9 ~]#
```

- `2756882` 就是 PID，若有 PID → **直接拿到 PID,跳到 Step 4**。
- 若只有 LISTEN 行、**没有 users 信息** → 占用进程在另一 PID namespace(容器内),宿主机看不到 PID,进入 Step 3。

### Step 3 —— 用 inode 反查 PID(看不到进程名时)

```bash
sudo find /proc/[0-9]*/fd -lname 'socket:[<inode>]' 2>/dev/null
# 例:
sudo find /proc/[0-9]*/fd -lname 'socket:[3816011173]' 2>/dev/null
```

输出形如 `/proc/2756882/fd/348`,其中 `2756882` 即占用进程 PID。

- **查不到** → 占用者用独立 PID namespace 且 hostPID 未开,宿主机不可见。改用容器运行时 CLI(Step 3.1)。

#### Step 3.1 —— 通过容器运行时定位

```bash
which docker crictl ctr          # 确认可用的 CLI
sudo crictl ps -a                # 列出本节点所有容器(含已停止)
# 或
sudo docker ps -a
```

根据应用名/application.jar 关键字筛出可疑容器,再查其 PID 与端口:

```bash
sudo crictl inspect <container-id> | grep -iE 'pid|port'
```

### Step 4 —— 确认占用进程身份(关键)

拿到 PID(本次为 `2756882`)后,逐项确认:

```bash
# 1) 启动命令:是不是自己的 jar / 同一个 application
sudo cat /proc/<PID>/cmdline | tr '\0' ' '; echo

# 2) cgroup:是否属于 k8s.io 容器,拿容器 ID
sudo cat /proc/<PID>/cgroup

# 3) 启动时间 / 已运行时长:判断是不是残留老进程(孤儿)
sudo ps -o pid,lstart,etime,cmd -p <PID>

# 4) 网络命名空间:是否等于宿主机初始 netns(hostNetwork 判据)
sudo ls -l /proc/<PID>/ns/net
```

判定要点:
| 证据 | 含义 |
|---|---|
| `cmdline` 含 `-jar .../application.jar` | 是自己的服务本体,非 sidecar |
| `cgroup` 路径含 `/k8s.io/<容器ID>` | 是 K8s 容器进程 |
| `etime` 远大于本次部署间隔(如 27 天) | **旧实例 / 孤儿进程**,非本应存在的实例 |
| `ns/net -> net:[4026531992]` | 宿主机初始网络命名空间 → **hostNetwork: true** |

### Step 5 —— 确认宿主机 IP 与网卡(验证 hostNetwork)

```bash
# 节点 IP
ip addr | grep <节点IP>
# 例:
ip addr | grep 192.168.100.123
```

若命中 `ens3` 等物理/虚拟网卡(非 `cni0`/`veth`/`calico`),且 `/proc/net/tcp` 中占用记录的本地地址正是该 IP → 坐实 hostNetwork。

### Step 6 —— 判断根因

结合 kubelet 日志确认是否"Pod 已删但容器未杀干净":

```bash
sudo systemctl status kubelet
sudo journalctl -u kubelet --since "1 hour ago" | grep -iE 'PLEG|StopPodSandbox|KillPodSandbox|failed'
```

典型孤儿征兆:

```
PLEG: Write status ...
Failed to stop sandbox ...
KillPodSandbox ... failed
```

→ kubelet/容器运行时状态不健康,旧容器被删但进程残留,成为占端口孤儿。

---

## 四、处理(清理)

> ⚠️ 杀进程前务必用 Step 4 确认它是**自己的旧实例 / 孤儿**,而非同节点其他在用服务。

### 4.1 杀掉孤儿进程

```bash
sudo kill <PID>
sudo kill -9 <PID>          # 不退则强杀
sudo ss -tlnp | grep 8085   # 验证端口已释放
```

### 4.2 清理对应容器(避免 kubelet 拉回 / 留脏 sandbox)

```bash
sudo crictl ps -a | grep <容器ID>
sudo crictl inspect <容器ID> | grep -iE 'podName|podNamespace'
# 必要时停/删容器
sudo crictl stop <容器ID>
sudo crictl rm <容器ID>
```

### 4.3 端口策略

- **优先**:清理孤儿后,把应用端口**改回平台约定的 8085**(保证网关 / Consul / 上游调用一致)。
- **临时绕过**:改用新端口(如 8086),但必须同步:
  - `server.port` = 新端口
  - `spring.cloud.consul.discovery.port` = 新端口(**不能只改 server.port**,否则 Consul 注册端口与实际监听不一致,下游连不上)
  - K8s manifest 的 `hostPort`(若有)= 新端口

> 简化做法:删除 `discovery.port`,让其自动跟随 `server.port`,只维护一处。

---

## 五、根因与治本

### 为什么 K8s 环境里"反复"遇到端口占用

1. **同 Pod 多容器抢端口**:多容器共享 network namespace,sidecar(网格/探针/本地代理)可能与业务撞同一端口。
2. **hostNetwork / hostPort**:端口升格为节点级资源,同节点多实例或旧实例极易冲突。
3. **kubelet 杀容器失败**:PLEG 异常 → `StopPodSandbox`/`KillPodSandbox` 失败 → 旧 java 进程变孤儿,继续占 hostNetwork 端口(本次根因)。
4. **固定端口 + 多副本**:多副本硬编码同一端口,hostNetwork 下必然撞。
5. **优雅关闭缺失**:滚动更新时 SIGTERM 未捕获 / preStop 未配,新老实例前后脚端口重叠。

### 治本措施

| 层面     | 措施                                                                                                                                      |
| -------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| 平台运维 | 不健康节点(hostNetwork 节点尤其)`drain` 后重启 containerd,清理孤儿容器;定期巡检 kubelet PLEG 报错                                         |
| 平台运维 | 建立容器内端口分配表,sidecar 端口与业务端口范围隔离                                                                                       |
| K8s 调度 | hostNetwork 服务优先打散到不同节点(反亲和),避免同节点多副本                                                                               |
| 应用配置 | 开启优雅关闭:`server.shutdown=graceful` + `spring.lifecycle.timeout-per-shutdown-phase=30s`;Pod 加 `preStop: sleep 10`;确认响应 `SIGTERM` |
| 应用配置 | 不要硬编码 `server.port` 与 `discovery.port` 两处,集中一处                                                                                |
| 排查习惯 | 容器内不用 `lsof`(常未装/不可用),直接 `cat /proc/net/tcp \| grep :<十六进制端口>`                                                         |

---

## 六、本次案例复盘

- **节点**:ant-k8snode-test-9(192.168.100.123)
- **占用进程**:PID 2756882,`java -Xms2048m -Xmx2048m ... -jar /home/container/app/application.jar`
- **特征**:hostNetwork(`ns/net -> net:[4026531992]`)、K8s 容器(`cgroup /k8s.io/406b...`)、已运行 **27 天**,为旧实例孤儿
- **根因**:kubelet PLEG 不健康,`KillPodSandbox` 失败,旧 Pod 容器删了但 java 进程残留,继续占 hostNetwork 8085;新版本部署到同节点 bind 8085 失败
- **处理**:kill 孤儿 + 清理 crictl 容器;临时改 8086 顶过(已同步 Consul discovery.port)
- **治本**:节点需 drain + 重启 containerd 清理;hostNetwork 服务做节点反亲和;应用加优雅关闭与 preStop
