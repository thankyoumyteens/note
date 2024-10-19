# setup

Vue 3 的 setup 函数是一个新增的组件选项, 它在 Composition API 中扮演了核心角色。用来替代 Vue 2 中的 Options API: data, computed, methods 和其他一些选项。

使用 setup 实现 vue 组件:

```vue
<script lang="ts">
export default {
  name: "HelloWorld",
  setup() {
    // setup中不能用this

    // 定义data
    // 注意: 此时msg是一个局部变量，不是响应式的
    // 修改msg不会触发视图更新
    let msg = "Hello World";

    // 定义methods
    function changeMsg() {
      msg = "Hello Vue 3";
    }

    // 返回data, methods, 供template使用
    return {
      // 要在这里返回才能在template中使用
      msg,
      changeMsg,
    };
  },
};
</script>

<template>
  <div>
    <h1>{{ msg }}</h1>
    <button @click="changeMsg">Change</button>
  </div>
</template>

<style scoped></style>
```

对应的 vue2 写法如下:

```vue
<script>
export default {
  name: "HelloWorld",
  data() {
    return {
      msg: "Hello World",
    };
  },
  methods: {
    changeMsg() {
      this.msg = "Hello Vue 3";
    },
  },
};
</script>

<template>
  <div>
    <h1>{{ msg }}</h1>
    <button @click="changeMsg">Change</button>
  </div>
</template>

<style scoped></style>
```

## 语法糖

在 script 标签中添加 setup, 相当于整个 script 标签都是一个 setup 函数并自动返回内部定义的变量, 这样就可以不用手动写 setup 函数和 return 了:

```vue
<script lang="ts">
// 组件名需要在setup外定义
export default {
  name: "HelloWorld",
};
</script>
<script lang="ts" setup>
// setup中不能用this
// import 导入的其它组件会自动注册, 不需要再写 components: {XxxXxx,}, 了

// 定义data
// 注意: 此时msg是一个局部变量，不是响应式的
// 修改msg不会触发视图更新
let msg = "Hello World";

// 定义methods
function changeMsg() {
  msg = "Hello Vue 3";
}
</script>

<template>
  <div>
    <h1>{{ msg }}</h1>
    <button @click="changeMsg">Change</button>
  </div>
</template>

<style scoped></style>
```
