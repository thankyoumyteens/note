# ref

reactive 可以定义基本类型和对象类型的响应式数据。

## 基本类型响应式

```vue
<script lang="ts" setup>
// 通过ref实现响应式
import { ref } from "vue";

// 定义data
// ref()函数接收一个基本类型的参数，返回一个响应式对象
let msg = ref("Hello Vue 3");

// 定义methods
function changeMsg() {
  // 修改ref对象的值, 需要通过.value属性
  // 此时Vue会自动更新视图
  msg.value = "Hello Vue 3.0";
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

## 对象类型响应式

```vue
<script lang="ts" setup>
// 通过ref实现响应式
import { ref } from "vue";

// 定义data
// ref()函数会返回一个响应式对象
let student = ref({
  name: "Tom",
  age: 18,
});

// 定义methods
function changeMsg() {
  // 修改ref对象的值, 需要通过.value属性
  // 此时Vue会自动更新视图
  student.value.name = "Jerry";
}
</script>

<template>
  <div>
    <h1>{{ student.name }}</h1>
    <button @click="changeMsg">Change</button>
  </div>
</template>

<style scoped></style>
```
