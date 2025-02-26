# 下拉刷新

```html
<script setup lang="ts">
  import { ref } from "vue";

  const isRefreshing = ref(false);

  const onRefresh = () => {
    // 开启下拉刷新动画
    isRefreshing.value = true;
    console.log("触发下拉刷新");
    // 模拟网络请求
    setTimeout(() => {
      // 关闭下拉刷新动画
      isRefreshing.value = false;
    }, 2000);
  };
</script>

<template>
  <view class="scroll-container">
    <!-- refresher-enabled 开启下拉刷新 -->
    <!-- refresher-triggered 是否展示下拉刷新动画 -->
    <scroll-view
      style="height: 100%"
      scroll-y
      refresher-enabled
      @refresherrefresh="onRefresh"
      :refresher-triggered="isRefreshing"
    >
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
