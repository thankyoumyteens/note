# nginx配置文件

```conf
# 启动Nginx工作进程的用户和组
user  nobody;
# 启动的工作进程数数量
worker_processes  2;

# 错误日志配置, 语法: error_log file [debug | info | notice | warn | error | crit | alert | emerg]
#error_log  logs/error.log;
#error_log  logs/error.log  notice;
#error_log  logs/error.log  info;

# pid文件保存路径
pid        logs/nginx.pid;

# 隐藏Nginx server版本
server_tokens off;

# 导入其他路径的配置文件
include /etc/nginx/conf.d/*.conf

events {
    #设置单个nginx工作进程可以接受的最大并发
    # 作为web服务器的时候最大并发数为 worker_connections * worker_processes
    # 作为反向代理的时候为 (worker_connections * worker_processes) / 2
    worker_connections  1024;
}

http {
    # 导入支持的文件类型
    include       mime.types;
    # 设置默认的类型
    default_type  application/octet-stream;

    # 日志格式
    log_format  main_formatter  '$remote_addr - $remote_user [$time_local] "$request" '
                                '$status $body_bytes_sent "$http_referer" '
                                '"$http_user_agent" "$http_x_forwarded_for" '
                                '"$upstream_addr" "$upstream_response_time"';
    
    # 不记录访问日志
    access_log  off;
    # 设置访问日志: access_log path [format [buffer=size] [gzip[=level]] [flush=time] [if=condition]];
    #access_log  logs/access.log  main_formatter;

    # 作为web服务器的时候打开sendfile加快文件传输
    sendfile        on;
    # 在开启了sendfile的情况下, 合并请求后统一发送给客户端
    #tcp_nopush     on;

    # 设置会话保持时间, 单位是秒
    keepalive_timeout  65;

    # 开启文件压缩
    #gzip  on;

    # 配置上游服务器, 实现负载均衡
    upstream microservice1 {
        server 127.0.0.1:8000 weight=1 fail_timeout=100 max_fails=3;
#        check interval=3000 rise=2 fall=5 timeout=1000;
    }
    
    upstream microservice2 {
        server 127.0.0.1:9999 weight=1 fail_timeout=10 max_fails=3;
#        check interval=3000 rise=2 fall=5 timeout=1000;
    }

    server {
        # 配置server监听的端口
        listen       7776;
        server_name  localhost;
        # 设置编码格式, 默认是俄语格式, 可以改为utf-8
        #charset koi8-r;
        # 自定义访问日志
        #access_log  logs/microservice.access.log  main_formatter;
        # 限制请求体的大小, 若超过所设定的大小, 返回413错误
        client_max_body_size 50m;

        # 处理接收到的请求
        location /microservice1/ {
            # 转发到负载均衡服务器
            proxy_pass http://microservice1;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "Upgrade";
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarder-For $proxy_add_x_forwarded_for;
            proxy_set_header Host $host:$server_port;
            proxy_set_header X-Nginx-Proxy true;
            # 配置当上游返回失败时候的重试机制
            proxy_next_upstream off;
        }

        location /microservice2/ {
            proxy_pass http://microservice2;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "Upgrade";
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarder-For $proxy_add_x_forwarded_for;
            proxy_set_header Host $host:$server_port;
            proxy_set_header X-Nginx-Proxy true;
            proxy_next_upstream off;
        }
    }
    
    server {
        listen       8081;
        server_name  localhost;
        
        location / {
            # 默认页面的目录名, 默认是相对路径
            root html;
            #默认页面的文件名
            index index.html index.htm;
        }
        
        #代理登录接口
        location /login {
            proxy_pass http://microservice1/login;
            proxy_cookie_path / /;
            proxy_set_header host $host;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header referer "-";
            proxy_redirect default;
            proxy_connect_timeout 90;
            proxy_send_timeout 90;
            proxy_read_timeout 90;
        }

        # 转发前端页面
        location /ui/ {
            # 设置别名
            alias   /home/html/frontend/;
            # 按指定的file顺序查找存在的文件, 并使用第一个找到的文件进行请求处理
            # 查找路径是按照给定的root或alias为根路径来查找的
            try_files $uri $uri/ /index.html /;
            index  index.html;
        }
    }
}
```
