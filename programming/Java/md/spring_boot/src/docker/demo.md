# 简单体验

让我们通过一个完整的例子来体验 Docker 的便捷。我们将拉取一个 Nginx 服务器镜像，并将其运行起来。

### 1. 拉取 Nginx 镜像

```sh
docker pull nginx
```

### 2. 运行 Nginx 容器

这里我们将本机的 8080 端口映射到容器内的 80 端口，并在后台运行。

```sh
docker run -d -p 8080:80 --name my-web-server nginx
```

### 3. 验证是否成功

打开你的浏览器，访问 [http://localhost:8080](http://localhost:8080)。如果你看到了 "Welcome to nginx!" 的欢迎页面，说明你的容器已经成功运行了！

### 4. 清理环境

测试完毕后，你可以停止并删除这个容器。

```sh
# 停止容器
docker stop my-web-server

# 删除容器
docker rm my-web-server
```
