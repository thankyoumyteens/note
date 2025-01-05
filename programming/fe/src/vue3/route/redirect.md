# 重定向

```ts
import { createRouter, createWebHistory } from "vue-router";

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: "/home",
      name: "Home",
      component: () => import("@/components/route-demo/Home.vue"),
      props: true,
    },
    {
      path: "/",
      // 当访问根路径时, 重定向到 /home
      redirect: "/home",
    },
  ],
});

export default router;
```
