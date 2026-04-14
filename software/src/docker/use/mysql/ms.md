# 搭建 MySQL 主从复制

在 MySQL 8.0 中，部分主从同步的专用语法有了更新（例如 SLAVE 关键字被替换为 REPLICA）。

### 1. 准备目录

我们需要为 Master（主节点）和 Slave（从节点）分别准备配置。请在你的宿主机上创建一个空文件夹（例如 ~/tmp/mydata/mysql-cluster），并在其中建立如下目录结构：

```
mysql-cluster/
├── master/
│   └── conf/
│       └── my.cnf
├── slave/
│   └── conf/
│       └── my.cnf
└── docker-compose.yml
```

### 2. 编写 Master 节点的 my.cnf

主节点的核心任务是开启二进制日志（Binlog），并拥有一个全局唯一的 ID。

编辑 master/conf/my.cnf：

```ini
[mysqld]
# 设置唯一的节点 ID，主节点通常设为 1
server-id=1
# 开启二进制日志，这是主从同步的核心凭证
log-bin=mysql-bin
# 设置字符集
character-set-server=utf8mb4
collation-server=utf8mb4_unicode_ci
```

### 3. 编写 Slave 节点的 my.cnf

从节点需要有不同的 ID，并且通常设置为只读模式（防止程序意外把数据写进从库，导致数据不一致）。

编辑 slave/conf/my.cnf：

```ini
[mysqld]
# 必须和主节点不同
server-id=2
# 设置为只读模式（注意：拥有 SUPER 权限的 root 用户依然可以写，但这能防住普通业务账号）
read_only=1
character-set-server=utf8mb4
collation-server=utf8mb4_unicode_ci
```

### 4. 编写 docker-compose.yml

将两个数据库编排在一起，放在同一个自定义网络中，这样它们就能通过容器名字（mysql-master 和 mysql-slave）互相找到对方，而不需要死记硬背 IP 地址。

在 mysql-cluster 目录下创建 docker-compose.yml：

```yaml
version: "3.8"

networks:
  mysql-net:
    driver: bridge

services:
  master:
    image: mysql:8.0
    container_name: mysql-master
    ports:
      - "3307:3306" # 映射到宿主机的 3307 端口，防止冲突
    environment:
      - MYSQL_ROOT_PASSWORD=rootpassword
    volumes:
      - ./master/conf/my.cnf:/etc/mysql/conf.d/my.cnf
      - ./master/data:/var/lib/mysql
    networks:
      - mysql-net

  slave:
    image: mysql:8.0
    container_name: mysql-slave
    ports:
      - "3308:3306" # 映射到宿主机的 3308 端口
    environment:
      - MYSQL_ROOT_PASSWORD=rootpassword
    volumes:
      - ./slave/conf/my.cnf:/etc/mysql/conf.d/my.cnf
      - ./slave/data:/var/lib/mysql
    networks:
      - mysql-net
    depends_on:
      - master # 确保主节点先启动
```

### 5. 运行命令一键启动

```sh
docker-compose up -d
```

### 5. 配置 Master (主库)

容器都跑起来后，我们需要进入主库，创建一个专门用于同步数据的账号，并查看当前的日志坐标。

```sh
docker exec -it mysql-master mysql -uroot -prootpassword
```

在 MySQL 命令行中逐条执行：

```sql
-- 创建一个名为 'repl' 的账号，允许任何 IP 连接，密码为 'replpassword'
CREATE USER 'repl'@'%' IDENTIFIED BY 'replpassword';

-- 赋予该账号专门的复制权限
GRANT REPLICATION SLAVE ON *.* TO 'repl'@'%';

-- 刷新权限使其生效
FLUSH PRIVILEGES;
```

获取主库状态 (极其重要！)

```sql
SHOW MASTER STATUS;
```

你会看到一个表格，请牢记或复制前两列的值（你的可能和下面不一样）：

- File: 比如 mysql-bin.000003
- Position: 比如 856

记下这两个值后，输入 `exit;` 退出主库。

### 6. 配置 Slave (从库)并开启同步

现在，我们要告诉从库：你的主库是谁、用什么账号连接、从哪个文件的哪个位置开始同步数据。

```sh
docker exec -it mysql-slave mysql -uroot -prootpassword
```

在 MySQL 8.0.23 及更高版本中，推荐使用 `CHANGE REPLICATION SOURCE TO` 替代老版本的 `CHANGE MASTER TO`。在命令行中执行（注意替换为你刚刚记下的 File 和 Position）：

```sql
CHANGE REPLICATION SOURCE TO
  SOURCE_HOST='mysql-master',      -- 指向 docker-compose 中的主库服务名
  SOURCE_USER='repl',              -- 刚才在主库创建的同步账号
  SOURCE_PASSWORD='replpassword',  -- 同步账号的密码
  SOURCE_LOG_FILE='mysql-bin.000003', -- 替换为你的 File 名字
  SOURCE_LOG_POS=856;                 -- 替换为你的 Position 数字
```

启动同步程序

```sql
-- 启动从库复制进程 (老版本是 START SLAVE)
START REPLICA;
```

执行以下命令查看从库状态：

```sql
-- 注意：\G 是为了让排版竖向显示，更易读。老版本命令为 SHOW SLAVE STATUS \G;
SHOW REPLICA STATUS \G;
```

在输出的这一大堆信息中，重点寻找以下两行：

- Replica_IO_Running: Yes (负责与主库通信，拉取日志)
- Replica_SQL_Running: Yes (负责执行拉取过来的日志，把数据写进自己库里)

只要这两个都是 Yes，恭喜你，主从架构搭建大功告成！

## 解决 Replica_IO_Running 状态是 Connecting 的问题

正常情况下，当你执行完 `START REPLICA;` 后，这个状态应该在一两秒内瞬间变成 **`Yes`**。如果一直卡在 `Connecting`（连接中），说明**从库正在尝试连接主库，但是网络不通或者被拒绝了**。

在 Docker 环境下，通常是以下三个原因之一导致的。我们来一步步排查：

### 定位问题

不要盲目猜，我们直接让“从库”去连接一下“主库”试试看。

请打开你的终端，直接运行这条命令（让 slave 容器以 repl 账号去登录 master 容器）：

```bash
docker exec -it mysql-slave mysql -h mysql-master -urepl -preplpassword
```

根据这条命令的返回结果，我们就能知道到底是哪里出了问题：

---

### 情况一：提示 `Unknown MySQL server host 'mysql-master'`

- **原因分析：** 网络不通。从库根本找不到名为 `mysql-master` 的机器。
- **解决办法：**
  1. 检查你的 `docker-compose.yml` 文件，确认两个服务是否在同一个 `networks` 下。
  2. 检查 `CHANGE REPLICATION SOURCE TO` 语句中的 `SOURCE_HOST` 拼写是否正确，有没有多加空格或者写错了名字。

### 情况二：提示 `Access denied for user 'repl'@'...' (using password: YES)`

- **原因分析：** 账号密码错误，或者主库没有开放权限。门找到了，但钥匙不对。
- **解决办法：**
  1. 确认你在配置从库时，`SOURCE_PASSWORD` 是否和主库创建时完全一致。
  2. 回到**主库**容器，确认你是否漏敲了刷新权限的命令。去主库补一刀：
     ```sql
     FLUSH PRIVILEGES;
     ```

### 情况三：能成功进入 MySQL 命令行 (出现 `mysql>`)

- **原因分析：** 网络是通的，密码也是对的！那为什么还会 `Connecting`？这通常是因为**主库的 3306 端口没对从库开放**，或者**遇到了 Docker 下经典的 UUID 冲突问题**。
- **经典坑点（UUID 冲突）：** 如果你在准备数据卷挂载目录时，图省事把主库的 `data` 目录直接复制给了从库，会导致两个库拥有相同的 `server-uuid`（记录在 `data/auto.cnf` 文件中）。MySQL 发现来连接的人和自己 UUID 一样，会认为是见鬼了，从而拒绝连接。
- **解决办法：**
  1. 进入从库所在宿主机的挂载目录 `./slave/data`。
  2. 看看有没有一个叫 `auto.cnf` 的文件，如果有，**直接删除它**。
  3. 重启从库容器：`docker restart mysql-slave`。

---

### 调整后如何重新启动同步？

当你根据上面的情况修复了问题后，回到**从库**的 MySQL 命令行中，执行以下命令重新启动同步进程：

```sql
-- 1. 先停止卡住的同步进程
STOP REPLICA;

-- (如果你需要修改账号密码或 IP，可以在这里重新执行 CHANGE REPLICATION SOURCE TO 语句)

-- 2. 再次启动同步
START REPLICA;

-- 3. 查看状态
SHOW REPLICA STATUS \G;
```
