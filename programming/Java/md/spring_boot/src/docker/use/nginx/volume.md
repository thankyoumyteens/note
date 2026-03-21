# 目录挂载

在实际生产环境中，我们绝对不能把网页文件和配置文件直接写死在容器里。如果容器被删除，数据就全丢了。我们需要把宿主机的目录挂载 (Volume) 到容器内部。

我们需要挂载三个核心目录：网页目录（html）、配置目录（conf）和日志目录（logs）。

### 1. 在宿主机创建所需目录

假设我们在 `~/tmp/mydata/nginx` 目录下统一管理：

```sh
mkdir -p ~/tmp/mydata/nginx/html
mkdir -p ~/tmp/mydata/nginx/logs
mkdir -p ~/tmp/mydata/nginx/conf
```

### 2. 获取默认的 Nginx 配置文件

Nginx 容器启动时需要默认配置。我们可以先启动一个临时的 Nginx 容器，把它的配置文件拷贝出来，然后再删掉它。

```sh
# 随便启动一个名为 nginx-test 的容器
docker run --name nginx-test -d nginx

# 将容器内的 nginx.conf 拷贝到宿主机的 conf 目录
docker cp nginx-test:/etc/nginx/nginx.conf ~/tmp/mydata/nginx/conf/nginx.conf
# 将默认的配置文件夹也拷贝出来 (包含 default.conf 等)
docker cp nginx-test:/etc/nginx/conf.d ~/tmp/mydata/nginx/conf/conf.d

# 删除临时容器
docker stop nginx-test
docker rm nginx-test
```

### 3. 创建一个测试网页

在刚才创建的 html 目录下写一个自定义的首页，用来验证挂载是否成功。

```sh
echo '<h1>Hello, Docker Nginx! Volume Mapping works!</h1>' > ~/tmp/mydata/nginx/html/index.html
```

### 4. 启动最终版的 Nginx 容器

现在，我们要带着这些挂载的目录来启动容器：

```sh
docker run -d \
  -p 8080:80 \
  --name my-nginx \
  -v ~/tmp/mydata/nginx/html:/usr/share/nginx/html \
  -v ~/tmp/mydata/nginx/conf/nginx.conf:/etc/nginx/nginx.conf \
  -v ~/tmp/mydata/nginx/conf/conf.d:/etc/nginx/conf.d \
  -v ~/tmp/mydata/nginx/logs:/var/log/nginx \
  --restart always \
  nginx
```

参数解释：

- `-v`: 数据卷挂载。格式为 `-v 宿主机绝对路径:容器内绝对路径`。
- `--restart always`: 无论容器是因为什么原因退出（包括服务器重启），Docker 都会自动重启这个 Nginx 容器。

### 5. 验证是否成功

打开浏览器，访问你的服务器 IP 地址（如果是本地机器，访问 [http://localhost:8080](http://localhost:8080)）。只要看到 "Hello, Docker Nginx!..." 的页面，就说明成功了！以后你只需要修改 `~/tmp/mydata/nginx/html` 里面的文件，网页就会立刻更新。
