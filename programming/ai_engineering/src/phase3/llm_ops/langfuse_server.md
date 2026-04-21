# LangfuseV2搭建

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
