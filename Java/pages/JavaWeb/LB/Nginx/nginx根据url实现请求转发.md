# nginx根据url实现请求转发

打开配置文件
```
vim /etc/nginx/sites-enabled/default
```
修改配置
```conf
http {
    server {
            server_name example.com;

            location /a/ {
                proxy_pass http://127.0.0.1:8080/;
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
            location /b/ {
                proxy_pass http://127.0.0.1:9090/;
            }
            location /ui/a {
                alias   /home/html/app/;
                try_files $uri $uri/ /index.html /;
                index  index.html; 
            }
    }
}
```

# proxy_set_header host $host

把源请求头中的host值放到转发的请求

# proxy_cookie_path

解决反向代理 cookie 丢失的问题

cookie 的 path 与地址栏上的 path 不一致浏览器就不会接受这个 cookie，无法传入 JSESSIONID 的 cookie，导致登录验证失败

```
proxy_cookie_path source target;
```
- source 源路径
- target 目标路径


# proxy_pass

该指令是用来设置代理服务器的地址，可以是主机名称，IP地址加端口号等形式

proxy_pass分为两种类型

1. 一种是只包含IP和端口号的 如`proxy_pass http://localhost:8080` 这种方式称为不带URI方式
2. 另一种是在端口号之后有其他路径的 如`proxy_pass http://localhost:8080/` 或 `proxy_pass http://localhost:8080/abc`  这种方式称为带URI方式

## 对于不带URI方式

nginx将会保留location中路径部分，比如：
```
location /api1/ {
    proxy_pass http://localhost:8080;
}
```
在访问`http://localhost/api1/1.jpg`时，会代理到`http://localhost:8080/api1/1.jpg`

## 对于带URI方式

nginx将对URL进行替换，比如：
```
location /api2/ {
    proxy_pass http://localhost:8080/;
}
```
当访问`http://localhost/api2/1.jpg`时，会代理到`http://localhost:8080/1.jpg`

又比如：
```
location /api5/ {
    proxy_pass http://localhost:8080/haha;
}
```

当访问`http://localhost/api5/1.jpg`时，会代理到`http://localhost:8080/haha1.jpg`
