# 轮播图

```html
<script setup lang="ts">
  const pictures: Array<{ id: number; url: string }> = [
    {
      id: 1,
      url: "/static/1.png",
    },
    {
      id: 2,
      url: "/static/2.png",
    },
    {
      id: 3,
      url: "/static/3.png",
    },
  ];

  const onChange = (e: any) => {
    // e.detail.current是pictures数组的下标
    console.log(`正在展示第${e.detail.current + 1}张图`);
  };

  const onPreviewImage = (url: string) => {
    console.log(url);
    // 预览图片
    uni.previewImage({
      current: url,
      urls: [url],
    });
  };
</script>

<template>
  <!-- 轮播图 -->
  <!-- indicator-dots="true" 显示面板指示点 -->
  <!-- autoplay="true" 自动切换, :interval="5000" 自动切换时间间隔 -->
  <!-- circular="true" 播放到末尾后重新回到开头 -->
  <swiper
    class="banner"
    indicator-dots
    autoplay
    circular
    :interval="5000"
    @change="onChange"
  >
    <swiper-item v-for="item in pictures" :key="item.id">
      <!-- @tap 点击事件 -->
      <image
        :src="item.url"
        mode="aspectFill"
        @tap="onPreviewImage(item.url)"
      ></image>
    </swiper-item>
  </swiper>
</template>

<style lang="scss">
  .banner {
    width: 100%;
    height: 200px;

    image {
      /* 图片占满 */
      width: 100%;
      height: 200px;
    }
  }
</style>
```
