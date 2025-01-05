# subscribe

```html
<script lang="ts" setup>
  import { useUserStore } from "./store/user";
  import { storeToRefs } from "pinia";
  const userStore = useUserStore();
  // 当userStore中的值发生变化时, 会触发回调函数
  userStore.$subscribe((mutation, state) => {
    console.log("mutation", mutation);
    console.log("修改后的值: ", state.name, state.age);
  });

  const change = () => {
    userStore.name = "new name";
  };
</script>

<template>
  <div>
    <button @click="change">change</button>
  </div>
</template>

<style scoped></style>
```
