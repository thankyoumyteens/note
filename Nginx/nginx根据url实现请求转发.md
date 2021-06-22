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
