# 配置别名

```conf
location /img/ {
    alias /var/www/image/;
}
```

## alias和root的区别

若用alias的话，则访问/img/目录里面的文件时，ningx会自动去/var/www/image/目录找文件，

比如：http://localhost/img/a.png 则是对应到服务器下的 /var/www/image/a.png

```conf
location /img/ {
    alias /var/www/image/;
}
```

若用root的话，则访问/img/目录下的文件时，nginx会去/var/www/image/img/目录下找文件,

比如：http://localhost/img/a.png 则是对应服务器下的 /var/www/image/img/a.png

```conf
location /img/ {
    root /var/www/image;
}
```

# nginx根据url实现请求转发

```conf
http {
    server {
            location /a/ {
                # 设置代理服务器的地址
                proxy_pass http://127.0.0.1:8080/;
                # 解决反向代理cookie丢失的问题
                proxy_cookie_path / /;
                # 把源请求头中的host值放到转发的请求头中
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

# proxy_cookie_path

反向代理cookie丢失问题: cookie的path与地址栏上的path不一致时，浏览器就不会接受这个cookie，无法传入JSESSIONID，导致登录验证失败

```
proxy_cookie_path source target;
```
- source 源路径
- target 目标路径

# proxy_pass

该指令是用来设置代理服务器的地址

## 不带URI参数

nginx将会保留location中路径部分，比如：

```conf
location /api1/ {
    proxy_pass http://localhost:8080;
}
```

在访问`http://localhost/api1/1.jpg`时，会代理到`http://localhost:8080/api1/1.jpg`

## 带URI参数

nginx将对URL进行替换，比如：

```conf
location /api2/ {
    # URI参数: /
    proxy_pass http://localhost:8080/;
}
```

当访问`http://localhost/api2/1.jpg`时，会代理到`http://localhost:8080/1.jpg`

又比如：

```conf
location /api5/ {
    # URI参数: /haha
    proxy_pass http://localhost:8080/haha;
}
```

当访问`http://localhost/api5/1.jpg`时，会代理到`http://localhost:8080/haha1.jpg`
