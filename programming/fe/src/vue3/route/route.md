# VueRouter

1. 安装:

```sh
npm install vue-router --save
```

2. 配置路由 src/router/index.ts

```ts
import { createRouter, createWebHistory } from "vue-router";

const router = createRouter({
  history: createWebHistory(), // 指定路由模式
  routes: [
    {
      path: "/home",
      name: "Home",
      component: () => import("@/components/route-demo/Home.vue"),
    },
    {
      path: "/about",
      name: "About",
      component: () => import("@/components/route-demo/About.vue"),
    },
  ],
});

export default router;
```

3. 修改 src/main.ts

```ts
import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";

const app = createApp(App);
// 注册路由
app.use(router);
app.mount("#app");
```

4. 修改 src/App.vue

```vue
<script lang="ts" setup></script>

<template>
  <div>
    <!-- 使用router-link切换路由 -->
    <router-link to="/home">Home</router-link>
    <router-link to="/about">About</router-link>

    <!-- 使用router-view展示路由组件 -->
    <router-view />
  </div>
</template>

<style scoped></style>
```
