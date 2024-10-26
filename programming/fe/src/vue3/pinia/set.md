# 修改 state 的值

```html
<script lang="ts" setup>
  import { useUserStore } from "./store/user";
  // 通过useUserStore获取userStore
  const userStore = useUserStore();

  // 修改userStore中的name
  const changeName = () => {
    userStore.name = "new name";
  };
</script>

<template>
  <div>
    <button @click="changeName">change name</button>
  </div>
</template>

<style scoped></style>
```

## 批量修改

```ts
import { useUserStore } from "./store/user";
// 通过useUserStore获取userStore
const userStore = useUserStore();

// 批量修改userStore中的数据
const change = () => {
  userStore.$patch({ name: "new name", age: 20 });
};
```
