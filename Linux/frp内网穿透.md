# 自己有域名的配置

## frps.ini服务端配置
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

## frpc.ini客户端配置
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
# 没有域名的配置

## frps.ini服务端配置
```conf
[common]
bind_addr = 0.0.0.0
bind_port = 7000
privilege_token = 12345678
```

## frpc.ini客户端配置
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
