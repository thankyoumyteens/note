# reactive

reactive 只能定义对象类型的响应式数据。

## 对象类型响应式

```html
<script lang="ts" setup>
  // 通过reactive实现响应式
  import { reactive } from "vue";

  // 定义data
  // reactive会将对象、数组、函数转换为响应式对象
  let student = reactive({
    name: "Tom",
    age: 18,
  });

  // 定义methods
  function changeMsg() {
    // 此时Vue会自动更新视图
    student.name = "Jerry";
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
