# watch

```vue
<script lang="ts" setup>
import { ref, watch } from "vue";

let student = ref({
  name: "Tom",
  age: 18,
});

let studentInfo = ref("");

watch(
  student,
  (newVal, oldVal) => {
    studentInfo.value = `Name: ${newVal.name}, Age: ${newVal.age}`;
  },
  {
    deep: true, // 要监视对象内部的字段变化时需要加上
    immediate: true, // 数据初始化时立即执行
  }
);

function changeName() {
  student.value.name = "Jerry";
}
</script>

<template>
  <div>
    <h1>{{ studentInfo }}</h1>
    <button @click="changeName">Change</button>
  </div>
</template>

<style scoped></style>
```
