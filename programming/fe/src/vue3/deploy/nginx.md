# nginx

## vue 配置

在 vite.config.js（Vite 项目）或 vue.config.js（Vue CLI 项目）中设置：

```js
// Vite 项目（vite.config.js）
export default defineConfig({
  base: "/my-app/", // 默认为 '/'，如果部署在子路径（如 http://domain/my-app），需改为 '/my-app/'
  // ...
});

// Vue CLI 项目（vue.config.js）
module.exports = {
  publicPath: "/my-app/", // 同上，子路径需对应修改
  // ...
};
```

publicPath 的值需与 Nginx 中配置的 location 路径一致。例如：若 Nginx 部署在 /my-app 路径下，则 publicPath 必须设为 `/my-app/`，否则资源会被解析到错误路径（如 `/js/xxx.js` 而非 `/my-app/js/xxx.js`）。

## nginx 配置

```conf
server {
    location /my-app/ {
        alias /usr/share/nginx/html/my-app/;
        try_files $uri $uri/ /my-app/index.html;
        index  index.html;
    }
}
```
