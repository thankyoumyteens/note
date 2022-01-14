# http

## 自己有域名

### frps.ini服务端配置
```conf
[common]
bind_addr = 0.0.0.0
bind_port = 7000
privilege_token = 12345678
vhost_http_port = 1180
vhost_https_port = 11443
```
启动
```
./frps -c frps.ini
```
或者
```
nohup ./frps -c frps.ini &
```

### frpc.ini客户端配置
```conf
[common]
server_addr = 服务端IP
server_port = 7000
privilege_token = 12345678

[httpname]
type = http
local_port = 8080
local_ip = 127.0.0.1
custom_domains = www.123.com

[httpsname]
type = https
local_port = 8081
local_ip = 127.0.0.1
custom_domains = www.456.com
```
启动
```
./frpc -c frpc.ini
```
此时访问 http://www.123.com:1180 或 https://www.456.com:11443 就可以打开本地的项目了

## 没有域名的配置

### frps.ini服务端配置
```conf
[common]
bind_addr = 0.0.0.0
bind_port = 7000
privilege_token = 12345678
```

### frpc.ini客户端配置
```conf
[common]
server_addr = 服务端IP
server_port = 7000
privilege_token = 12345678

[httpname]
type = tcp
local_port = 80
local_ip = 127.0.0.1
remote_port = 8080
```

## 二级域名内网穿透

### 在域名解析后台配置子域名
登录域名的解析后台，在123.com下增加A记录: test,记录值为部署frp服务端的公网服务器的ip。


### frps.ini服务端配置
```conf
[common]
# frp监听的端口，用作服务端和客户端通信
bind_port = 7000
# 服务端通过此端口监听和接收公网用户的http请求
vhost_http_port = 7071
# frp提供了一个控制台，可以通过这个端口访问到控制台。可查看frp当前有多少代理连接以及对应的状态
# dashboard_port = 7500
# 服务端的subdomain_host需要和客户端配置文件中的subdomain、local_port配合使用，
# 可通过{subdomain}.{subdomain_host} 的域名格式来访问自己本地的 web 服务。
# 假如服务端的subdomain_host为dev.msh.com，客户端某个配置组中的
# subdomain为a,local_port为8585，
# 则访问 a.dev.msh.com ，等同于访问本地的localhost:8585
subdomain_host = test.123.com
```
启动
```
nohup ./frps -c frps.ini &
```

### nginx反向代理实现二级域名转发
```conf
server {
    listen 80;
    server_name 123.com www.123.com;
    location / {
			root /home/website;
			index index.html;
    }
}
# 二级域名转发
server {
    listen 80;
    server_name test.123.com;
    location / {
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header Host $http_host;
        proxy_pass http://127.0.0.1:7071;
    }
}
```

### frpc.ini客户端配置
```conf
[common]
server_addr = 服务端IP
server_port = 7000
privilege_token = 12345678

[httpname]
type = http
local_port = 8080
local_ip = 127.0.0.1
custom_domains = test.123.com
```
启动
```
./frpc -c frpc.ini
```
此时访问 http://test.123.com 就可以打开本地的项目了,访问 http://123.com 仍是服务器原本的项目

