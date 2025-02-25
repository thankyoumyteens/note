# 滚动触底

```html
<script setup lang="ts">
  const onScrollToLower = () => {
    console.log("滚动触底了");
  };
</script>

<template>
  <view class="scroll-container">
    <scroll-view style="height: 100%" scroll-y @scrolltolower="onScrollToLower">
      <view v-for="index in 100">占位{{index}}</view>
    </scroll-view>
  </view>
</template>

<style lang="scss" scoped>
  page {
    height: 100%;
    display: flex;
    flex-direction: column;
  }

  .scroll-container {
    flex: 1;
    overflow-y: auto;
  }
</style>
```
