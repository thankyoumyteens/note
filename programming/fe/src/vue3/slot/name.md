# 具名插槽

1. 父组件

```html
<script lang="ts" setup>
  import Child from "./Child.vue";
</script>

<template>
  <div>
    <Child>
      <template v-slot:title>
        <h1>标题</h1>
      </template>
      <template v-slot:content>
        <p>内容</p>
      </template>
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
    <slot name="title"></slot>
    <slot name="content"></slot>
  </div>
</template>

<style scoped></style>
```

## v-slot 简写

```html
<script lang="ts" setup>
  import Child from "./Child.vue";
</script>

<template>
  <div>
    <Child>
      <template #title>
        <h1>标题</h1>
      </template>
      <template #content>
        <p>内容</p>
      </template>
    </Child>
  </div>
</template>

<style scoped></style>
```
