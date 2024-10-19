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

let nameInH2 = ref();

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
  <div>
    <h1 ref="nameInH2">{{ student.name }}</h1>
    <button @click="getName">button</button>
  </div>
</template>

<style scoped></style>
```

父组件使用:

```vue
<script setup lang="ts">
import HelloWorld from "./components/HelloWorld.vue";
import { ref } from "vue";

const hello = ref();

const getHello = () => {
  // 使用子组件暴露出的变量和函数
  console.log(hello.value.student.name);
  console.log(hello.value.getName());
};
</script>

<template>
  <div>
    <HelloWorld ref="hello" />
    <button @click="getHello">button</button>
  </div>
</template>

<style scoped></style>
```
