# 避免访问静态文件时直接下载

修改 nginx 配置:

```conf
# 配置根目录下的文件访问
location = /.well-known/apple-app-site-association {
    # 关键：将MIME类型设置为JSON
    default_type application/json;
    # 可选：如果文件是静态文件，指定其路径
    alias /path/to/your/apple-app-site-association;
}
```

重载配置:

```sh
nginx -s reload
```
