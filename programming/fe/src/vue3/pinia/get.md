# 读取 state 的值

```html
<script lang="ts" setup>
  import { useUserStore } from "./store/user";
  // 通过useUserStore获取userStore
  const userStore = useUserStore();
</script>

<template>
  <div>
    <!-- 使用userStore中的数据 -->
    <div>{{ userStore.name }}</div>
    <div>{{ userStore.age }}</div>
  </div>
</template>

<style scoped></style>
```

## 取出响应式数据

```html
<script lang="ts" setup>
  import { useUserStore } from "./store/user";
  import { storeToRefs } from "pinia";
  // 通过useUserStore获取userStore
  const userStore = useUserStore();

  // 将name和age转换为ref对象
  const { name, age } = storeToRefs(userStore);
</script>

<template>
  <div>
    <!-- 使用userStore中的数据 -->
    <div>{{ name }}</div>
    <div>{{ age }}</div>
  </div>
</template>

<style scoped></style>
```
