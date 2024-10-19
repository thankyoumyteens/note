# watchEffect

```vue
<script lang="ts" setup>
import { reactive, watchEffect } from "vue";

let student = reactive({
  name: "Tom",
  age: 18,
});

watchEffect(() => {
  // 类似于计算属性, 当函数中用到的变量的值有修改, 就会触发
  if (student.name === "Jerry") {
    console.log("Jerry is here");
  }
});

function changeName() {
  student.name = "Jerry";
}
</script>

<template>
  <div>
    <h1>{{ student.name }}</h1>
    <button @click="changeName">Change</button>
  </div>
</template>

<style scoped></style>
```
