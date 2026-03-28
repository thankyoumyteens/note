# 使用 Docker Compose

### 1. 创建 docker-compose.yml 文件

在你喜欢的目录下（比如 ~/tmp/mydata/mysql），确保同级目录下有 conf/my.cnf，然后创建 docker-compose.yml：

```yaml
version: "3.8"

services:
  mysql:
    image: mysql:8.0
    container_name: my-mysql
    restart: always
    ports:
      - "3306:3306"
    environment:
      - MYSQL_ROOT_PASSWORD=your_strong_password
      - TZ=Asia/Shanghai # 设置时区为东八区
    volumes:
      - ./data:/var/lib/mysql
      - ./conf/my.cnf:/etc/mysql/conf.d/my.cnf
      - ./logs:/var/log/mysql
    # 限制日志大小，防止时间长了撑爆服务器硬盘
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

### 2. 一键启动

在文件所在目录执行：

```sh
docker-compose up -d
```
