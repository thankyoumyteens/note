# 使用 Docker Compose

虽然 docker run 命令很强大，但当参数变多时，命令行会变得非常长且难以维护。在实际工作中，我们通常使用 `docker-compose.yml` 文件来管理。

### 1. 创建 docker-compose.yml 文件

在你喜欢的目录下（例如 `~/tmp/mydata/nginx`）创建一个名为 `docker-compose.yml` 的文件，填入以下内容：

```yaml
version: "3.8"

services:
  nginx:
    image: nginx:latest
    container_name: my-nginx-compose
    ports:
      - "8080:80"
    volumes:
      - ./html:/usr/share/nginx/html
      - ./conf/nginx.conf:/etc/nginx/nginx.conf
      - ./conf/conf.d:/etc/nginx/conf.d
      - ./logs:/var/log/nginx
    restart: always
    environment:
      - TZ=Asia/Shanghai # 设置时区，保证日志时间正确
```

注意：这里使用了相对路径 `./`，这意味着你的 html、conf 等文件夹需要和 docker-compose.yml 文件在同一个目录下。

### 2. 一键启动

在这个文件所在的目录下，运行：

```sh
docker-compose up -d
```

### 3. 停止并删除容器

想要停止并删除容器，只需运行：

```sh
docker-compose down
```

这种方式不仅清晰明了，还可以将其放入 Git 代码库中进行版本控制。
