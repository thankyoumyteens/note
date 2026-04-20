# LangfuseV2搭建

Langfuse 是一个专为大语言模型（LLM）应用打造的开源可观测性（Observability）和评估平台。 在传统的 Java 后端时代，你排查问题看的是 Log、查的是数据库、用的是 SkyWalking。但在 AI 时代，大模型的输入和输出全是大段的自然语言，且充满不确定性。
如果把你的 AI Agent 比作一架超音速客机，Langfuse 就是这架飞机的“黑匣子”+“塔台雷达”。

1. 核心底座：极其变态的全链路追踪 (Tracing)。当你的 Python 脚本接收到用户的提问：“查一下订单 ORD-002”，Langfuse 会帮你记录下这极其复杂的生命周期：
   - Trace（整体追踪）：记录这通对话总共花了 3 秒，花了 0.05 美元。
   - Generation（大模型生成）：记录 Python 到底把这个订单号包装成了什么样的 Prompt 发给了 OpenAI/Claude，大模型又返回了怎样一坨带着 Tool Call 的 JSON。
   - Span（普通逻辑耗时）：记录大模型决定调用工具后，你的 Python 请求 Java MCP 接口花了多少毫秒，Java 吐回来的业务数据长什么样。
   - 价值：一旦 AI 答错了，你打开后台，一层层点开，一眼就能定案到底是提示词写得烂，还是 Java 接口背了锅。
2. 拔高利器：提示词版本管理 (Prompt Management)。在初级阶段，大家都是把 Prompt 写死在 Python 代码的字符串里（Hardcode）。
   - Langfuse 允许你在它的 Web 后台像写代码一样管理 Prompt。
   - 你可以在后台修改 Prompt，打上 v2、v3 的标签，然后在 Python 代码里直接通过 SDK 动态拉取最新的 Prompt。
   - 价值：提示词的优化（调参）彻底与代码部署解耦。产品经理甚至可以直接在后台修改 Prompt 优化 AI 语气，而不需要你重新发版！
3. 终极闭环：量化评估与指标大盘 (Evaluation & Metrics)
   - 领导问你：“咱们接入大模型后，回答准确率是多少？每天大概烧多少钱？”
   - Langfuse 会自动帮你汇总 Token 开销大盘、首字延迟（TTFT）。
   - 它还支持给每一条回答打分（比如用户点了👍或👎，或者你通过自动化脚本判断它有没有出现“幻觉”）。
   - 价值：让 AI 系统的优化从“我觉得还行”变成“准确率从 85% 提升到了 92%，Token 成本下降了 15%”。

Langfuse 官方极其厚道地提供了完整的 Docker 镜像。我们不需要去搞复杂的 Kubernetes，在本地或者开发机上，一个干净的 `docker-compose.yml` 就能把这台“行车记录仪”的指挥中心拔地而起。

### 1. 编写基建编排文件 (Docker Compose)

在你的电脑上新建一个目录（比如 `langfuse-local`），在里面新建一个 `docker-compose.yml` 文件。直接贴入这套极简但绝对够用的标准架构：

```yaml
services:
  langfuse-server:
    # 🌟 抛弃坑爹的 latest，死死锁在纯粹的 V2 版本！
    image: ghcr.io/langfuse/langfuse:2
    depends_on:
      - db
    ports:
      - "3000:3000"
    restart: always
    environment:
      # 数据库连接串, 格式是: 协议://用户名:密码@主机名:端口/数据库名。注意主机名是 db，
      # Docker 内部自带 DNS，会自动把db解析到下面那个数据库容器的内网 IP
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/postgres
      # 基于 Next.js 框架的加密盐。它用来加密你的登录 Cookie 和 Session。（随便敲几个长字符串即可）
      - NEXTAUTH_SECRET=my_super_secret_key_for_langfuse_2026
      - SALT=my_super_salt_for_langfuse_2026
      # 对外提供服务的地址
      - NEXTAUTH_URL=http://localhost:3000
      # 关闭官方的匿名数据收集，彻底断开与外网的脐带。
      - TELEMETRY_ENABLED=false

  db:
    # 选择极其成熟稳定的 PostgreSQL 15 版本
    image: postgres:15
    restart: always
    environment:
      # 给数据库设置初始的超管账号、密码和默认创建的数据库名
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_DB=postgres
    volumes:
      # 把容器内部真正存数据的目录，映射到外面一个叫 langfuse_postgres_data 的数据卷里
      - langfuse_postgres_data:/var/lib/postgresql/data

volumes:
  # 在系统底层申请一块不会随容器销毁而消失的存储空间，名字就叫 langfuse_postgres_data
  langfuse_postgres_data:
```

### 2. 基座点火

打开终端，进入该目录，敲下这行指令：

```bash
docker-compose up -d
```

稍等几十秒，让 Postgres 数据库完成初始化，随后 Langfuse 的 Web 引擎就会在 3000 端口接客。

### 3. 初始化你的私有空间

1.  浏览器打开：`http://localhost:3000`
2.  你会看到 Langfuse 的注册页面。因为是本地私有数据库，**大胆地注册你的管理员账号**（比如用你的常用邮箱）。
3.  登录后，新建一个 Project（例如 `MCP-Java-Local`）。
4.  在项目的左侧导航栏找到 **API Keys**，点击 Create new API keys。
    - 复制生成的 `Secret Key` 和 `Public Key`。
