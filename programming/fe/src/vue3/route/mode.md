# 路由模式

## history 模式

优点：URL 更加美观，不带有 `＃`，更接近传统的网站 URL。

缺点：后期项目上线，需要服务端配合处理路径问题，否则刷新会有 404 错误。

```ts
const router = createRouter({
  history: createWebHistory(),
  routes: [],
});
```

## hash 模式

优点：兼容性更好，因为不需要服务器端处理路径。

缺点：URL 带有 `＃` 不美观，且在 SEO 优化方面相对较差。

```ts
const router = createRouter({
  history: createWebHashHistory(),
  routes: [],
});
```
