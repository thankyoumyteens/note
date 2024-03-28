# last-child无效

```html
<template>
  <div class="root-container">
    <div class="father">
      <div class="child" v-for="item in 10" :key="item">
        一共10个元素, 我是第{{item}}个
        <template v-if="item== 10">(css控制我的颜色)</template>
      </div>
      <p>我是多余的元素</p>
    </div>
  </div>
</template>
<style lang="scss" scoped>
  .father {
    width: 500px;
    border: 1px solid #b2b6b6;
    text-align: center;
    .child {
      padding: 10px 0;
      &:last-child {
        color: red;
      }
    }
  }
</style>
```

el:last-child 的匹配规则

1. 查找 el 选择器匹配元素的所有同级元素
2. 在同级元素中查找最后一个元素
3. 检验最后一个元素是否与选择器el匹配

因为`.child:last-child`匹配到的最后一个元素是p标签而不是`.child`, 所以last-child无效了。

# 解决办法

- 让:last-child在其父元素内没有其它的标签, 即让其父元素仅包含该种类型标签
- 使用其它标签选择器: last-of-type
