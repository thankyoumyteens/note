# 集成 vuex

1. 安装

```sh
npm install vuex@3 --save
```

2. 创建 store/index.js

```js
import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

const store = new Vuex.Store({
  state: {
    // 定义一个name, 以供全局使用
    name: "张三",
    // 定义一个number, 以供全局使用
    number: 0,
    // 定义一个list, 以供全局使用
    list: [
      { id: 1, name: "111" },
      { id: 2, name: "222" },
      { id: 3, name: "333" },
    ],
  },
});

export default store;
```

3. 修改 main.js

```js
import Vue from "vue";
import App from "./App.vue";
import store from "./store";

Vue.config.productionTip = false;
new Vue({
  store, // 把store对象添加到vue实例上
  render: (h) => h(App),
}).$mount("#app");
```

4. 使用

```vue
<template>
  <div id="app"></div>
</template>

<script>
export default {
  name: "App",
  mounted() {
    // 使用this.$store.state.xxx可以直接访问到仓库中的状态
    console.log(this.$store.state.name);
  },
};
</script>

<style></style>
```

## 避免每次都写 this.$store.state.xxx

```vue
<template>
  <div id="app"></div>
</template>

<script>
import { mapState } from "vuex";
export default {
  name: "App",
  mounted() {
    // 直接获取
    console.log(this.name);
  },
  computed: {
    // 把this.$store.state.name自动添加到计算属性中
    ...mapState(["name"]),
  },
};
</script>

<style></style>
```
