# 集成 vue-router

1. 安装

```sh
npm install vue-router@^3.5.2
```

2. 新建 router/index.js 文件

```js
import Vue from "vue";
import VueRouter from "vue-router";

Vue.use(VueRouter);

//定义路由的集合
const routes = [
  {
    path: "/home",
    name: "home",
    component: () => import("../components/Home.vue"),
  },
  {
    path: "/words",
    name: "words",
    component: () => import("../components/WordsEditor.vue"),
  },
];

const router = new VueRouter({
  //hash模式路由
  mode: "hash",
  base: process.env.BASE_URL,
  routes,
});

export default router;
```

3. 修改 main.js

```js
import Vue from "vue";
import App from "./App.vue";
import router from "./router";

Vue.config.productionTip = false;
new Vue({
  router, // 把router对象添加到vue实例上
  render: (h) => h(App),
}).$mount("#app");
```

3. 使用

```vue
<template>
  <div id="app">
    <router-link to="/words">跳转</router-link>
    <router-view />
  </div>
</template>

<script>
export default {
  name: "App",
};
</script>

<style></style>
```
