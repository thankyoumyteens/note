# 登陆校验

1. 在 router/index.js 中校验

```js
import Vue from "vue";
import VueRouter from "vue-router";
import store from "@/store";

Vue.use(VueRouter);

const routes = [
  {
    path: "/home",
    name: "home",
    component: () => import("../components/Home.vue"),
  },
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

// 导航守卫
router.beforeEach((to, from, next) => {
  // 登陆验证
  if (to.path !== "/login" && !store.state.user.isLogin) {
    next({ path: "/login" });
  } else {
    next();
  }
});

export default router;
```
