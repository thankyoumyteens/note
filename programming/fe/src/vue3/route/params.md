# router-link 传参

1. 传递参数

```html
<script lang="ts" setup>
  let param1 = "ok";
</script>

<template>
  <div>
    <!-- 使用字符串的形式传递参数 -->
    <router-link :to="`/home?param1=${param1}`">Home</router-link>
    <!-- 使用对象的形式传递参数 -->
    <router-link
      :to="{
        path: '/home',
        query: {
          param1: param1,
        },
      }"
    >
      Home
    </router-link>

    <router-view />
  </div>
</template>

<style scoped></style>
```

2. 接收参数

```html
<script lang="ts" setup>
  import { useRoute } from "vue-router";
  import { toRefs } from "vue";
  // 通过useRoute获取路由信息
  const route = useRoute();
  // 通过route.query获取参数
  const { query } = toRefs(route);
</script>

<template>
  <!-- 使用route中传来的参数 -->
  <div>{{ query.param1 }}</div>
</template>

<style scoped></style>
```
