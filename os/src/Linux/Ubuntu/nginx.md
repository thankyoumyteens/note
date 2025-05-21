# 安装依赖包

```sh
sudo apt-get -y install gcc libpcre3 libpcre3-dev zlib1g zlib1g-dev openssl libssl-dev
```

# 下载安装包

```sh
cd ~/src_pack
wget http://nginx.org/download/nginx-1.25.2.tar.gz
tar -xvf nginx-1.25.2.tar.gz
```

# 编译

```sh
cd nginx-1.25.2
sudo ./configure --prefix=/usr/local/nginx --pid-path=/usr/local/nginx/logs/nginx.pid --error-log-path=/usr/local/nginx/logs/error.log --http-log-path=/usr/local/nginx/logs/access.log --with-http_ssl_module
sudo make
sudo make install
```

configure参数含义: 

- `--prefix=/usr/local/nginx` 安装路径
- `--pid-path=/usr/local/nginx/logs/nginx.pid` 进程文件
- `--error-log-path=/usr/local/nginx/logs/error.log` 错误日志路径
- `--http-log-path=/usr/local/nginx/logs/access.log` 访问日志路径
- `--with-http_ssl_module` 启用http ssl 安全访问模块

# 启动nginx

```sh
/usr/local/nginx/sbin/nginx
```

# 停止nginx

```sh
/usr/local/nginx/sbin/nginx -s stop
```
