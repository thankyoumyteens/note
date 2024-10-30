# 作用域插槽

子组件通过插槽向父组件传值。

1. 父组件

```html
<script lang="ts" setup>
  import Child from "./Child.vue";
</script>

<template>
  <div>
    <Child>
      <template #title="params">
        <h1>{{ params.titleData }}</h1>
      </template>
      <template #content="params">
        <p>{{ params.contentData }}</p>
      </template>
    </Child>
  </div>
</template>

<style scoped></style>
```

2. 子组件

```html
<script lang="ts" setup>
  import { ref } from "vue";

  const title = ref("标题");
  const content = ref("内容");
</script>

<template>
  <div>
    <slot name="title" :titleData="title"></slot>
    <slot name="content" :contentData="content"></slot>
  </div>
</template>

<style scoped></style>
```
