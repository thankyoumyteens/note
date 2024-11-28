# createBrowserRouter 部署

### 1. 路由中指定 basename

```ts
const routeOptions = {
  basename: "/",
};

if (process.env.NODE_ENV !== "development") {
  routeOptions.basename = "/my-app";
}
// 定义路由
const router = createBrowserRouter(routes, routeOptions);
```

### 2. 配置 nginx

```ini
server {
    location /my-app/ {
        alias /usr/share/nginx/html/my-app/;
        try_files $uri $uri/ /my-app/index.html;
        index  index.html;
    }
}
```
