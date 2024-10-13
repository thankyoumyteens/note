# 修改值

类似于 java 中的 setXxx 方法

1. 定义 mutation

```js
import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

const store = new Vuex.Store({
  state: {
    menuList: [],
  },
  mutations: {
    setMenuList(state, menuList) {
      state.menuList = menuList;
    },
  },
});

export default store;
```

2. 使用

```vue
<template>
  <div id="app"></div>
</template>

<script>
export default {
  name: "App",
  methods: {
    initMenu(menuList) {
      this.$store.commit("setMenuList", menuList);
    },
  },
};
</script>

<style></style>
```
