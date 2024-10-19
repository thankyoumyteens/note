# HTML 标签

```vue
<script lang="ts" setup>
import { reactive, ref } from "vue";

let student = reactive({
  name: "Tom",
  age: 18,
});

// 相当于 let nameInH2 = this.$refs['nameInH2']
let nameInH2 = ref();

function getName() {
  student.name = "Jerry";
  console.log(nameInH2.value);
}
</script>

<template>
  <div>
    <h1 ref="nameInH2">{{ student.name }}</h1>
    <button @click="getName">button</button>
  </div>
</template>

<style scoped></style>
```
