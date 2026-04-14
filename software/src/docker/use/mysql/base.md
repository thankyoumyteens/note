# 最基础的 MySQL 运行

### 1. 拉取 MySQL 镜像

建议指定版本（目前最通用的是 8.0），不建议数据库使用 latest 标签，以防未来版本大更新导致兼容性问题：

```sh
docker pull mysql:8.0
```

### 2. 启动容器

注意：MySQL 容器启动时必须设置 root 用户的密码，否则容器会自动退出。

```sh
docker run -d \
  --name my-mysql \
  -p 3306:3306 \
  -e MYSQL_ROOT_PASSWORD=your_strong_password \
  mysql:8.0
```

参数解释：

- `-e MYSQL_ROOT_PASSWORD=...`: 通过环境变量（`-e`）设置 root 用户的初始密码。
- `-p 3306:3306`: 将宿主机的 3306 端口映射到容器的 3306 端口。
