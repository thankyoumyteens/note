# LangfuseV3搭建

### 1. 编写基建编排文件 (Docker Compose)

在你的电脑上新建一个目录（比如 `langfuse-v3`），在里面新建一个 `docker-compose.yml` 文件。直接贴入这套极简但绝对够用的标准架构：

```yaml
services:
  # ==========================================
  # 1. 基础设施层：Zookeeper & ClickHouse (大数据分析引擎)
  # ==========================================
  zookeeper:
    image: zookeeper:3.9
    ports:
      - "2181:2181"
    restart: always
    volumes:
      - langfuse_v3_zk_data:/data
      - langfuse_v3_zk_datalog:/datalog

  clickhouse:
    image: clickhouse/clickhouse-server:23.8
    depends_on:
      - zookeeper
    restart: always
    environment:
      - CLICKHOUSE_DB=default
      - CLICKHOUSE_USER=default
      - CLICKHOUSE_PASSWORD=clickhouse_secret_2026
      - CLICKHOUSE_DEFAULT_ACCESS_MANAGEMENT=1
    ports:
      - "8123:8123"
      - "19000:9000"
    volumes:
      - langfuse_v3_ch_data:/var/lib/clickhouse
      - ./clickhouse-cluster.xml:/etc/clickhouse-server/config.d/cluster.xml

  # ==========================================
  # 2. 基础设施层：PostgreSQL (关系型元数据)
  # ==========================================
  db:
    image: postgres:15
    restart: always
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_DB=postgres
    volumes:
      - langfuse_v3_pg_data:/var/lib/postgresql/data

  # ==========================================
  # 3. 基础设施层：Redis (高速消息队列)
  # ==========================================
  redis:
    image: redis:7
    # 启动时强行要求密码认证
    command: redis-server --requirepass redis_super_secret_2026
    restart: always
    ports:
      - "6379:6379"

  # ==========================================
  # 4. 基础设施层：MinIO (私有化 S3 对象存储)
  # ==========================================
  minio:
    image: minio/minio
    command: server /data --console-address ":9001"
    restart: always
    ports:
      - "9000:9000" # API 端口
      - "9001:9001" # 控制台端口
    environment:
      - MINIO_ROOT_USER=minioadmin
      - MINIO_ROOT_PASSWORD=minioadmin123
    volumes:
      - langfuse_v3_minio_data:/data

  # 这个短命容器只负责在系统启动时，自动帮你把 'langfuse-events' 存储桶建好
  minio-setup:
    image: minio/mc
    depends_on:
      - minio
    entrypoint: >
      /bin/sh -c "
      sleep 5;
      /usr/bin/mc config host add myminio http://minio:9000 minioadmin minioadmin123;
      /usr/bin/mc mb myminio/langfuse-events || true;
      exit 0;
      "

  # ==========================================
  # 5. 应用层：Langfuse Web (前台指挥官)
  # ==========================================
  langfuse-server:
    image: ghcr.io/langfuse/langfuse:3
    depends_on:
      - db
      - clickhouse
      - minio
      - redis
    restart: always
    ports:
      - "3003:3000"
    environment: &langfuse_env # 🌟 YAML 锚点技术：抽取公共配置，传给 Worker
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/postgres
      - CLICKHOUSE_URL=http://clickhouse:8123
      - CLICKHOUSE_MIGRATION_URL=clickhouse://clickhouse:9000
      - CLICKHOUSE_USER=default
      - CLICKHOUSE_PASSWORD=clickhouse_secret_2026
      - CLICKHOUSE_CLUSTER_ENABLED=true
      - NEXTAUTH_SECRET=my_v3_super_secret
      - SALT=my_v3_super_salt
      - NEXTAUTH_URL=http://localhost:3003
      - TELEMETRY_ENABLED=false

      # 🌟 Redis 队列配置
      - REDIS_HOST=redis
      - REDIS_PORT=6379
      # 🌟 给 Langfuse 塞入刚刚设置的 Redis 密码
      - REDIS_AUTH=redis_super_secret_2026

      # 🌟 MinIO/S3 泄洪通道配置
      - LANGFUSE_S3_EVENT_UPLOAD_BUCKET=langfuse-events
      - LANGFUSE_S3_EVENT_UPLOAD_ENDPOINT=http://minio:9000
      - LANGFUSE_S3_EVENT_UPLOAD_REGION=us-east-1 # MinIO 的伪装区域
      - LANGFUSE_S3_EVENT_UPLOAD_ACCESS_KEY_ID=minioadmin
      - LANGFUSE_S3_EVENT_UPLOAD_SECRET_ACCESS_KEY=minioadmin123
      - LANGFUSE_S3_EVENT_UPLOAD_FORCE_PATH_STYLE=true

  # ==========================================
  # 6. 应用层：Langfuse Worker (后台搬砖工)
  # ==========================================
  langfuse-worker:
    image: ghcr.io/langfuse/langfuse-worker:3
    depends_on:
      - langfuse-server
    restart: always
    environment: *langfuse_env # 🌟 继承上方 Web 节点的所有环境变量

volumes:
  langfuse_v3_pg_data:
  langfuse_v3_ch_data:
  langfuse_v3_minio_data:
  langfuse_v3_zk_data:
  langfuse_v3_zk_datalog:
```

### 2. 在本地创建“神经桥梁”文件

在你存放 docker-compose.yml 的同一个文件夹里，新建一个名为 clickhouse-cluster.xml 的文件，把这段纯正的企业级集群配置贴进去：

```xml
<clickhouse>
    <zookeeper>
        <node>
            <host>zookeeper</host>
            <port>2181</port>
        </node>
    </zookeeper>

    <remote_servers>
        <default>
            <shard>
                <replica>
                    <host>clickhouse</host>
                    <port>9000</port>
                </replica>
            </shard>
        </default>
    </remote_servers>

    <macros>
        <shard>01</shard>
        <replica>01</replica>
    </macros>
</clickhouse>
```

### 3. 拉升 Docker 宿主机资源配额

在 Mac 环境下跑企业级微服务集群，默认的资源配置是绝对扛不住的。

1. 拔掉当前引擎的电源

```sh
colima stop
```

2. 重装上阵：注入 12G 纯粹算力

```sh
# 12G 内存，外加 4 核 CPU！
colima start --memory 12 --cpu 4
```

### 4. 基座点火

打开终端，进入该目录，敲下这行指令：

```bash
docker-compose up -d
```

### 5. 初始化你的私有空间

1.  浏览器打开：`http://localhost:3003`
2.  你会看到 Langfuse 的注册页面。因为是本地私有数据库，**大胆地注册你的管理员账号**（比如用你的常用邮箱）。
3.  登录后，新建一个 Project（例如 `MCP-Java-Local`）。
4.  在项目的左侧导航栏找到 **API Keys**，点击 Create new API keys。
    - 复制生成的 `Secret Key` 和 `Public Key`。

### 6. 创建存储桶

1. 打开浏览器，访问我们刚才暴露出来的宿主机控制台端口：http://localhost:9001
   - 账号：minioadmin
   - 密码：minioadmin123
2. 登录后，你大概率会发现 Buckets 列表是空的。点击 Create Bucket 按钮
3. 在 Bucket Name 栏里，精准输入之前在 docker-compose.yml 里写死的名字: langfuse-events
4. 点击 Create（其他高级选项如 Quota/Versioning 全都不用管，保持默认）
