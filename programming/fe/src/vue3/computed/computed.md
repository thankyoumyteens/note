# 计算属性

```vue
<script lang="ts" setup>
import { reactive, computed } from "vue";

let student = reactive({
  name: "Tom",
  age: 18,
});

let studentInfo = computed(() => {
  return `${student.name} is ${student.age} years old`;
});

function changeName() {
  student.name = "Jerry";
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
