# 轮播图

```html
<template>
  <!-- 轮播图 -->
  <!-- indicator-dots="true" 显示面板指示点 -->
  <!-- autoplay="true" 自动切换, :interval="1000" 自动切换时间间隔 -->
  <!-- circular="true" 播放到末尾后重新回到开头 -->
  <swiper class="banner" autoplay circular :interval="1000">
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

<script>
  export default {
    data() {
      return {
        // 轮播图列表
        pictures: [
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
        ],
      };
    },
    onLoad() {},
    methods: {
      onPreviewImage(url) {
        console.log(url);
        // 预览图片
        uni.previewImage({
          current: url,
          urls: [url],
        });
      },
    },
  };
</script>

<style>
  .banner {
    width: 100%;
    height: 200px;
  }

  .banner image {
    /* 图片占满 */
    width: 100%;
    height: 200px;
  }
</style>
```
