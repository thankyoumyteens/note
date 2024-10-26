# Pinia

Pinia 用来代替 Vuex。

1. 安装

```sh
npm install pinia
```

2. 在 main.ts 中注册

```ts
import { createApp } from "vue";
import App from "./App.vue";
// 引入pinia
import { createPinia } from "pinia";

const app = createApp(App);
// 创建pinia实例
const pinia = createPinia();
// 注册pinia
app.use(pinia);
app.mount("#app");
```
