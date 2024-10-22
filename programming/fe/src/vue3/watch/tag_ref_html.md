# HTML 标签

```vue
<script lang="ts" setup>
import { ref } from "vue";

// 相当于 let demo = this.$refs['demo']
const demo = ref();

setTimeout(() => {
  // <p>ok</p>
  console.log(demo.value);
}, 1000);
</script>

<template>
  <div>
    <p ref="demo">ok</p>
  </div>
</template>

<style scoped></style>
```
