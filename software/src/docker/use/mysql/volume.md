# 数据持久化与自定义配置

数据库的数据和配置决不能随容器的删除而丢失。我们需要将宿主机的目录挂载到容器内部。

### 1. 在宿主机创建所需目录

我们通常需要挂载三个目录：数据目录（data）、配置目录（conf）和日志目录（logs）。

```sh
mkdir -p ~/tmp/mydata/mysql/data
mkdir -p ~/tmp/mydata/mysql/conf
mkdir -p ~/tmp/mydata/mysql/logs
```

### 2. 准备自定义配置文件 (my.cnf)

MySQL 8.0 默认已经比较好用了，但我们通常会显式地设置字符集为 utf8mb4，以完美支持中文和 Emoji 表情。

在 `~/tmp/mydata/mysql/conf` 目录下创建 `my.cnf` 文件：

```sh
vim ~/tmp/mydata/mysql/conf/my.cnf
```

填入以下基础配置：

```ini
[client]
default-character-set=utf8mb4

[mysql]
default-character-set=utf8mb4

[mysqld]
# 设置字符集为 utf8mb4
character-set-server=utf8mb4
collation-server=utf8mb4_unicode_ci
init_connect='SET NAMES utf8mb4'

# 忽略表名大小写 (视你的开发习惯而定，1为忽略，Linux下默认为0严格区分)
lower_case_table_names=1
```

### 3. 带着挂载目录启动 MySQL

```sh
docker run -d \
  -p 3306:3306 \
  --name my-mysql \
  -v ~/tmp/mydata/mysql/log:/var/log/mysql \
  -v ~/tmp/mydata/mysql/data:/var/lib/mysql \
  -v ~/tmp/mydata/mysql/conf/my.cnf:/etc/mysql/conf.d/my.cnf \
  -e MYSQL_ROOT_PASSWORD=your_strong_password \
  --restart always \
  mysql:8.0
```

关键参数：

- `-v ~/tmp/mydata/mysql/data:/var/lib/mysql`: 最重要的一步！ 将容器内存储真实数据的 `/var/lib/mysql` 映射到宿主机，这样就算你执行了 `docker rm -f my-mysql`，只要重新挂载这个目录，数据瞬间恢复。
