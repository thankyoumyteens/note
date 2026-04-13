# iOS 端静默断网抢救指南(FastAPI + Nginx 架构专属)

#### 👻 1. 经典症状特征（精准对号入座）

如果你在测试时，完美命中了以下 **4 条特征**，请直接跳过业务代码排查，直接上“核武器”：

1. **设备差异**：电脑端（PC Chrome）访问极其顺滑，唯独 iOS（或部分安卓）端疯狂报错。
2. **触发时机**：刚发版后，或者手机**隔了一段时间（比如半小时）没使用**，第一次点击必定报错。
3. **报错速度**：不是转圈圈转到超时，而是**0毫秒瞬间弹出**“网络异常”或拿不到响应数据。
4. **自愈玄学**：报错后，把手机放在旁边等大约一分钟（或开关一下飞行模式），再去点突然就好了。

#### 🕵️‍♂️ 2. 底层死因：NAT 墙与 WebKit 的“双向奔赴”

- **云端/运营商的 NAT 防火墙**：为了省资源，会把空闲超过一定时间（如 5 分钟）的 TCP 连接**静默剪断**（不发通知）。
- **iOS WebKit 底层引擎**：极其头铁，无视网络波动，强行复用连接池里那根已经被剪断的“僵尸 TCP 通道”发数据。
- **致命击杀**：服务器的 Linux 内核收到野包，瞬间回发 `TCP RST`（强制重置）报文。iOS 收到 RST，当场抛出 `ERR_NETWORK`，连重新握手都懒得做。

---

### ☢️ 3. 标准抢救流程 (SOP)

一旦确诊，不要去查跨域，不要查数据库，直接祭出以下“前端+服务端”双绝杀。

#### 🔪 第一刀：服务端 Nginx 彻底剥夺手机的 Keep-Alive 权利

别让手机觉得它可以保持长连接。强迫它每次都重新拨号。

**操作：** 打开 `nginx.conf`，找到对应站点的 `server` 或 `location` 块：

```nginx
# 极其关键：将保持时间设为 0，强制每次请求完立即销毁 TCP 连接
keepalive_timeout 0;
```

_执行 `nginx -s reload` 生效。_

#### 🔪 第二刀：前端 Axios 注入“破冰重发”拦截器

如果因为某种极端情况（比如刚发完请求 Nginx 还没来得及断），iOS 依然报了 `ERR_NETWORK`，前端绝不能弹窗，必须静默兜底。

**操作：** 在 Axios 的响应拦截器（`response.use` 的 `error` 分支）中，加入以下核心逻辑：

```typescript
if (error?.code === "ERR_NETWORK" && !error?.response) {
  const config = error?.config;

  // 确保没有死循环重发
  if (config && !config._retry) {
    config._retry = true;

    // 1. 等待 500ms，让 iOS 底层彻底抛弃死链接
    await new Promise((resolve) => setTimeout(resolve, 500));

    // 2. GET 请求挂载时间戳，骗过 WebKit 缓存，强行建立新 TCP 握手
    if (config.method?.toUpperCase() === "GET") {
      config.params = { ...config.params, _t: Date.now() };
    }

    // 3. 拿着新配置静默重发，用户完全无感
    return apiClient(config);
  }
}
```

#### 🛡️ 辅助防护：装配前端“透视镜”

永远不要在 `catch` 里只写一句 `toast.error('网络请求失败')`。移动端没有 F12，必须把底层的 `error.message` 和 `error.code`（如 `ERR_NETWORK` 还是 `ECONNABORTED`）直接打印在错误弹窗里，这是你下次排查的“唯一生命线”。

---

### 💡 架构认知升级 (为什么以前 Java 没这事？)

从这件事情上，我们可以提炼出一个极其宝贵的架构经验：
**永远不要完全信任移动端的网络环境，也永远不要假设网络通道是绝对可靠的。**

以前写 Spring Boot 时，庞大的 Tomcat 像保姆一样在底层做心跳检测、静默重试，帮你抗下了所有移动端的网络异动；现在你切到了 FastAPI/Go/Node.js 这种极简高性能架构，去掉了臃肿的容器，获得了极高的并发性能，但代价就是——**你必须亲自接管网络容错的指挥权**。
