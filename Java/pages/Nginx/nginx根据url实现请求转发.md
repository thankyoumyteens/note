# nginx根据url实现请求转发

打开配置文件
```
vim /etc/nginx/sites-enabled/default
```
修改配置
```
http {
    server {
            server_name example.com;

            location /mail/ {
                    proxy_pass http://example.com:protmail;
            }

            location /com/ {
                    proxy_pass http://127.0.0.1:8080/main;
            }

            location / {
                    proxy_pass http://example.com:portdefault;
            }
    }
}
```

# proxy_pass的注意事项

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
