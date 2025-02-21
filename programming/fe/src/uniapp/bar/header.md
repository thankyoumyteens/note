# 自定义顶部导航栏

### 1. CustomNavBar.vue

```html
<script setup lang="ts">
  // 获取屏幕边界的安全距离(适配各种刘海)
  const { safeAreaInsets } = uni.getSystemInfoSync();
  // 输出: {top: 10, right: 0, bottom: 0, left: 0}
  console.log(safeAreaInsets);
  // 适配各种刘海
  const navBarPadding = {
    paddingTop: `${safeAreaInsets?.top}px`,
  };
</script>

<template>
  <!-- style 适配各种刘海 -->
  <view class="nav-bar" :style="navBarPadding">
    <view class="text-lg font-bold">首页</view>
    <view class="flex items-center">
      <view class="text-gray-500 mr-2">消息</view>
      <view class="text-gray-500 mr-2">搜索</view>
    </view>
  </view>
</template>

<style lang="scss"></style>
```

### 2. index.vue

```html
<script setup lang="ts">
  import CustomNavBar from "./components/CustomNavBar.vue";
</script>

<template>
  <CustomNavBar />
</template>

<style lang="scss"></style>
```

### 3. pages.json

```json
{
  "pages": [
    {
      "path": "pages/index/index",
      "style": {
        // 隐藏默认顶部导航栏
        "navigationStyle": "custom",
        // 导航栏标题(手机通知栏)颜色，仅支持 black/white
        "navigationBarTextStyle": "white"
      }
    }
  ]
  // ...
}
```
