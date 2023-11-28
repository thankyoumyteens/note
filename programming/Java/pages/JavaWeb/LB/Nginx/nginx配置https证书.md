# 重新编译nginx添加ssl模块

```
./configure --with-http_ssl_module
```

# 准备SSL证书

`1_域名_bundle.crt`和`2_域名.key`

# 修改nginx的配置文件

```conf
http{
    server{
        #监听443端口
        listen 443;
        #对应的域名, 把baofeidyz.com改成你们自己的域名就可以了
        server_name 域名;

        ssl on;
        #第一个证书文件的全路径
        ssl_certificate /home/test/1_域名_bundle.crt;
        #第二个证书文件的全路径
        ssl_certificate_key /home/test/2_域名.key;
        ssl_session_timeout 5m;
        ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
        ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:HIGH:!aNULL:!MD5:!RC4:!DHE;
        ssl_prefer_server_ciphers on;

        location / {
            root /home/test/html;
            index index.html;
        }
    }
}
```

# 重启nginx
