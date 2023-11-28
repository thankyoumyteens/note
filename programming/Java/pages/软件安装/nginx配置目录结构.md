# nginx.conf

nginx.conf是配置文件的入口

基本内容: 
```conf
user www-data;
worker_processes auto;
pid /run/nginx.pid;
include /etc/nginx/modules-enabled/*.conf;

events {
    worker_connections 768;
}

http {
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    types_hash_max_size 2048;

    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    ssl_protocols TLSv1 TLSv1.1 TLSv1.2; # Dropping SSLv3, ref: POODLE
    ssl_prefer_server_ciphers on;

    access_log /var/log/nginx/access.log;
    error_log /var/log/nginx/error.log;

    gzip on;
    gzip_disable "msie6";

    include /etc/nginx/conf.d/*.conf;
    include /etc/nginx/sites-enabled/*;
}
```

其中有两行比较重要
```
include /etc/nginx/conf.d/*.conf;
include /etc/nginx/sites-enabled/*;
```
- 第一行表示把/etc/nginx/conf.d/这个目录下面所有以conf结尾的文件都当做配置文件引入
- 第二行表示把/etc/nginx/sites-enabled/下面所有的文件都当成配置文件引入

# sites-available

这个文件夹一般在需要建立和管理多个站点的时候非常有用

sites-available的所有文件都是从/etc/nginx/sites-available创建的软链接,而sites-available/文件夹里面是实实在在的配置文件

只有在 sites-enabled 目录下的配置文件才能够真正被用户访问。但是可以将文件放在 sites-available 目录下用来存档或者生成链接。

```
ln -s /etc/nginx/sites-available/myConf /etc/nginx/sites-enabled/myConf
```
