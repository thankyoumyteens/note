# 最基础的 Nginx 运行

### 1. 拉取 Nginx 官方镜像

你可以直接指定版本，或者拉取最新版（默认）：

```sh
docker pull nginx:latest
```

### 2. 启动 Nginx 容器

使用以下命令启动一个在后台运行的 Nginx：

```sh
docker run --name my-nginx -p 8080:80 -d nginx
```

参数解释：

- `--name my-nginx`: 给你的容器起个好记的名字。
- `-p 8080:80`: 端口映射。将宿主机（你的电脑/服务器）的 8080 端口映射到容器内的 80 端口。格式是 `宿主机端口:容器内端口`。
- `-d`: 让容器在后台（Detached mode）运行。
- `nginx`: 使用的镜像名称。

### 3. 验证是否成功

打开浏览器，访问你的服务器 IP 地址（如果是本地机器，访问 [http://localhost:8080](http://localhost:8080)）。只要看到 "Welcome to nginx!" 的页面，就说明搭建成功了！
