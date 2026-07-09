# 使用 Docker Compose

虽然 docker run 命令很强大，但当参数变多时，命令行会变得非常长且难以维护。在实际工作中，我们通常使用 `docker-compose.yml` 文件来管理。

### 1. 在宿主机创建所需目录

假设我们在 `~/mydata/nginx` 目录下统一管理：

```sh
mkdir -p ~/mydata/nginx/html
mkdir -p ~/mydata/nginx/logs
mkdir -p ~/mydata/nginx/conf
```

### 2. 获取默认的 Nginx 配置文件

Nginx 容器启动时需要默认配置。我们可以先启动一个临时的 Nginx 容器，把它的配置文件拷贝出来，然后再删掉它。

```sh
# 随便启动一个名为 nginx-test 的容器
docker run --name nginx-test -d nginx

# 将容器内的 nginx.conf 拷贝到宿主机的 conf 目录
docker cp nginx-test:/etc/nginx/nginx.conf ~/mydata/nginx/conf/nginx.conf
# 将默认的配置文件夹也拷贝出来 (包含 default.conf 等)
docker cp nginx-test:/etc/nginx/conf.d ~/mydata/nginx/conf/conf.d

# 删除临时容器
docker stop nginx-test
docker rm nginx-test
```

### 3. 创建一个测试网页

在刚才创建的 html 目录下写一个自定义的首页，用来验证挂载是否成功。

```sh
echo '<h1>Hello, Docker Nginx! Volume Mapping works!</h1>' > ~/mydata/nginx/html/index.html
```

### 4. 创建 docker-compose.yml 文件

在你喜欢的目录下（例如 `~/mydata/nginx`）创建一个名为 `docker-compose.yml` 的文件，填入以下内容：

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

### 5. 一键启动

在这个文件所在的目录下，运行：

```sh
docker-compose up -d
```

### 6. 停止并删除容器

想要停止并删除容器，只需运行：

```sh
docker-compose down
```

这种方式不仅清晰明了，还可以将其放入 Git 代码库中进行版本控制。
