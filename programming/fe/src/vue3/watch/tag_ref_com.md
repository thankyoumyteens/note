# 组件标签

父组件只能获取到子组件对外暴露的变量。

子组件暴露部分变量:

```vue
<script lang="ts" setup>
import { reactive, ref } from "vue";

let student = reactive({
  name: "Tom",
  age: 18,
});

function getName() {
  return student.name;
}

// 暴露部分变量和函数
defineExpose({
  student,
  getName,
});
</script>

<template>
  <div></div>
</template>

<style scoped></style>
```

父组件使用:

```vue
<script setup lang="ts">
import Child from "./components/Child.vue";
import { ref } from "vue";

// 相当于 let demo = this.$refs['demo']
const demo = ref();

const test = () => {
  // 使用子组件暴露出的变量和函数
  console.log(demo.value.student.name);
  console.log(demo.value.getName());
};
</script>

<template>
  <div>
    <Child ref="demo" />
    <button @click="test">button</button>
  </div>
</template>

<style scoped></style>
```
