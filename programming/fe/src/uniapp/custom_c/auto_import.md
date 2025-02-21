# 自动导入自定义组件

### 1. pages.json

```json
{
  // 自动导入自定义组件
  "easycom": {
    "autoscan": true,
    "custom": {
      // 遇到以My开头的标签, 就去@/components中寻找组件
      "^My(.+)": "@/components/My$1.vue"
    }
  }
  // ...
}
```

### 2. index.vue

```html
<script setup lang="ts"></script>

<template>
  <!-- 不用导入, 直接用 -->
  <MySwiper />
</template>

<style lang="scss"></style>
```
