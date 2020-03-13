# 配置Nginx

最新版本nginx配置是由4个文件构成: 
1. `conf.d`: 用户自己定义的conf配置文件
2. `sites-available`: 系统默认设置的配置文件
3. `sites-enabled`: 由sites-available中的配置文件转换生成
4. `nginx.conf`: 汇总以上三个配置文件的内容，同时配置我们所需要的参数

在部署需要的web服务时，我们可以拷贝`sites-enabled`中的`default`文件到`conf.d`并且修改名字为`**.conf`,然后进行配置, 配置好后需要删除`sites-enabled`中的`default`文件, 每次配置完成后, 都需要重启nginx

```
server {
    #服务启动时监听的端口
    listen 80 default_server;
    listen [::]:80 default_server;
    #服务启动时文件加载的路径
    root /var/www/html;
    #默认加载的第一个文件
    index index.php index.html index.htm index.nginx-debian.html;
    #页面访问域名，如果没有域名也可以填写_
    server_name www.xiexianbo.xin;

    location / {
        #页面加载失败后所跳转的页面
        try_files $uri $uri/ =404;
    }
    
    # 如果Apache的文档为root，则拒绝访问.htaccess文件
    location ~ /\.ht {
        deny all;
    }
}
```
