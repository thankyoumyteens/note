# visible.sync

父组件

```html
<note-menu :menuVisible.sync="menuVisible" />
```

子组件

```html
<template>
  <div>
    <el-drawer :visible.sync="menuVisible" :before-close="handleClose">
    </el-drawer>
  </div>
</template>

<script>
  export default {
    props: {
      menuVisible: {
        type: Boolean,
        default: false,
      },
    },
    methods: {
      handleClose() {
        this.$emit("update:menuVisible", false);
      },
    },
  };
</script>

<style></style>
```
