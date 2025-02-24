# 局部滚动

```html
<script setup lang="ts">
  import CustomNavBar from "./components/CustomNavBar.vue";
</script>

<template>
  <CustomNavBar />
  <MySwiper />
  <!-- 占满页面剩余高度 -->
  <!-- 不能把.scroll-container的样式直接写在scroll-view上, 不生效 -->
  <view class="scroll-container">
    <!-- scroll-y: 垂直方向滚动 -->
    <!-- height: 100% 必须加 -->
    <scroll-view style="height: 100%" scroll-y>
      <view v-for="index in 1000">占位{{index}}</view>
    </scroll-view>
  </view>
</template>

<style lang="scss" scoped>
  /* 
  page 样式是专门针对当前页面根节点的样式设置，
  UniApp 编译后生成的页面根节点默认类名为 page，
  通过 page 样式可以对整个页面(此处是index.vue)的背景、字体等基础样式进行统一设置 
  */
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
