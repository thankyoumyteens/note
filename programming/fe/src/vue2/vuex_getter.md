# 修饰器

类似于 java 中的 getXxx 方法

1. 定义 getter

```js
import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

const store = new Vuex.Store({
  state: {
    name: "admin",
  },
  getters: {
    getName(state) {
      return state.name + "123";
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
import { mapGetters, mapState } from "vuex";

export default {
  name: "App",
  mounted() {
    console.log(this.name); // admin
    console.log(this.getName); // admin123
  },
  computed: {
    ...mapState(["name"]),
    ...mapGetters(["getName"]),
  },
};
</script>

<style></style>
```
