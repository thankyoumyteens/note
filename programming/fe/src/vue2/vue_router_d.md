# 动态配置路由

1. 在 router/index.js 中定义基本路由

```js
import Vue from "vue";
import VueRouter from "vue-router";
import store from "@/store";

Vue.use(VueRouter);

// 定义基本路由
const routes = [
  {
    path: "/login",
    name: "login",
    component: () => import("../components/Login.vue"),
  },
];

const router = new VueRouter({
  mode: "hash",
  base: process.env.BASE_URL,
  routes,
});

export default router;
```

2. 修改 main.js

```js
import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import { getMenuList } from "@/api/menu";

Vue.config.productionTip = false;

// 从后端获取路由列表
getMenuList().then((res) => {
  const menuList = res.data;
  try {
    // 转换component
    const resolvedRoutes = menuList.map((route) => ({
      ...route,
      component: () => import(`@/components/${route.component}.vue`),
    }));
    // 添加路由
    router.addRoutes(resolvedRoutes);

    // 保存菜单
    store.commit("setMenuList", menuList);

    // 路由添加完, 再创建vue实例
    new Vue({
      router,
      store,
      render: (h) => h(App),
    }).$mount("#app");
  } catch (error) {
    console.error("Failed to setup dynamic routes:", error);
  }
});
```
