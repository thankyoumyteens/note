# 源码安装

## 安装依赖包

Ubuntu
```
sudo apt-get -y install gcc
sudo apt-get -y install libpcre3 libpcre3-dev
sudo apt-get -y install zlib1g zlib1g-dev
sudo apt-get -y install openssl
# Ubuntu14.04的仓库中没有发现openssl-dev，由libssl-dev替代
sudo apt-get -y install libssl-dev
```

CentOS
```
yum -y install gcc gcc-c++ automake zlib zlib-devel \
openssl openssl--devel pcre pcre-devel
```

## 安装nginx

下载安装包
```
cd /usr/local
mkdir nginx
cd nginx
wget http://nginx.org/download/nginx-1.13.7.tar.gz
tar -xvf nginx-1.13.7.tar.gz 
```

编译
```
/usr/local/nginx/nginx-1.13.7
sudo ./configure --prefix=/usr/local/nginx --pid-path=/usr/local/nginx/logs/nginx.pid --error-log-path=/usr/local/nginx/logs/error.log --http-log-path=/usr/local/nginx/logs/access.log --with-http_ssl_module
sudo make
sudo make install
```

- `--prefix=/usr/local/nginx` 安装路径
- `--pid-path=/usr/local/nginx/logs/nginx.pid` 进程文件
- `--error-log-path=/usr/local/nginx/logs/error.log` 错误日志路径
- `--http-log-path=/usr/local/nginx/logs/access.log` 访问日志路径
- `--with-http_ssl_module` 启用http ssl 安全访问模块

## 启动nginx

```
cd /usr/local/nginx/sbin
./nginx
```
