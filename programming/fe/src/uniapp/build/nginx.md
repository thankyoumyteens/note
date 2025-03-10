# nginx

### 1. manifest.json

1. 路由模式 选择 hash
2. 运行的基础路径 填写在 nginx 中的相对路径, 比如 `/my-app/`

### 2. nginx 配置

```conf
server {
    location /my-app/ {
        alias /usr/share/nginx/html/my-app/;
        try_files $uri $uri/ /my-app/index.html;
        index  index.html;
    }
}
```
