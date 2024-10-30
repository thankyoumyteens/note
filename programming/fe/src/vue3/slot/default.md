# 默认插槽

1. 父组件

```html
<script lang="ts" setup>
  import Child from "./Child.vue";
</script>

<template>
  <div>
    <Child>
      <span>hello</span>
    </Child>
  </div>
</template>

<style scoped></style>
```

2. 子组件

```html
<script lang="ts" setup></script>

<template>
  <div>
    <slot></slot>
  </div>
</template>

<style scoped></style>
```
