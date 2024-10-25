# 编程式路由导航

```html
<script lang="ts" setup>
  import { useRouter } from "vue-router";
  const router = useRouter();
  const jumpToHome = () => {
    // 跳转到Home
    router.push({ path: "/home", query: { param1: "value1" } });
  };
</script>

<template>
  <div>
    <button @click="jumpToHome">跳转到Home</button>
    <router-view />
  </div>
</template>

<style scoped></style>
```

## 不保留历史记录的跳转

```ts
const jumpToHome = () => {
  // 使用replace替代push
  router.replace({ path: "/home", query: { param1: "value1" } });
};
```
