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
                    proxy_pass http://example.com:protmail/;
            }

            location /com/ {
                    proxy_pass http://127.0.0.1:8080/main/;
            }

            location / {
                    proxy_pass http://example.com:portdefault;
            }
    }
}
```
以上的配置会按以下规则转发请求( GET 和 POST 请求都会转发):

- 将 http://example.com/mail/ 下的请求转发到 http://example.com:portmail/
- 将 http://example.com/com/ 下的请求转发到 http://example.com:portcom/main/
- 将其它所有请求转发到 http://example.com:portdefault/

需要注意的是，在以上的配置中，webdefault 的代理服务器设置是没有指定URI的，而 webmail 和 webcom 的代理服务器设置是指定了URI的(分别为 / 和 /main/)。

如果代理服务器地址中是带有URI的，此URI会替换掉 location 所匹配的URI部分。

而如果代理服务器地址中是不带有URI的，则会用完整的请求URL来转发到代理服务器。

以上配置的转发示例：
```
http://example.com/mail/index.html -> http://example.com:portmail/index.html
http://example.com/com/index.html -> http://example.com:portcom/main/index.html
http://example.com/mail/static/a.jpg -> http://example.com:portmail/static/a.jpg
http://example.com/com/static/b.css -> http://example.com:portcom/main/static/b.css
http://example.com/other/index.htm -> http://example.com:portdefault/other/index.htm
```
