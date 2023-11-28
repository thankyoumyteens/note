# z-index无效

```html
<!-- main -->
<template>
  <div class="w">
    <div>
      <!-- ... -->
      <div class="icon-btn" @click="openDrawer()">
        打开抽屉
      </div>
    </div>

    <el-drawer></el-drawer>
  </div>
</template>
<style lang="scss" scoped>
.icon-btn {
  position: fixed;
  bottom: 10px;
  right: 10px;
  z-index: 999999;
}
```


点击后, icon-btn会被el-drawer挡住, 无论z-index设置多大都没用。

## 原因

当fixed定位元素的DOM层级较深时, z-index会受到层叠上下文的影响, 无论z-index设置多大, 都无法超过父元素的层级。

## 解决方案

将fixed元素放到外层, 避免受到层叠上下文的影响, 可以把元素封装成vue自定义组件, 在mounted中动态插入到body下, 这样就可以避免受层叠上下文的影响了。


```html
<!-- main -->
<template>
  <div class="w">
    <top-div @openDrawer="openDrawer"></top-div>

    <el-drawer></el-drawer>
  </div>
</template>
```


```html
<!-- topDiv.vue -->
<template>
  <div>
    <div class="icon-btn" @click="openDrawer()">
    打开抽屉
    </div>
  </div>
</template>
<script>
export default {
  mounted() {
    const _dom = document.querySelector('body');
    // 将当前组件挂载到body下的最后
    _dom.insertBefore(this.$el, _dom.lastChild);
  },
  beforeDestroy() {
    // 从body中移除当前组件
    this.$el.remove();
  },
  methods: {
    openDrawer() {
      this.$emit('openDrawer');
    }
  }
};
</script>
<style lang="scss" scoped>
.icon-btn {
  position: fixed;
  bottom: 10px;
  right: 10px;
  z-index: 999999;
}
</style>
```
