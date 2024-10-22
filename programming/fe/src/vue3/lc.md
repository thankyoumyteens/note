# 组件的生命周期

- beforeCreate: 被 setup 替代
- created: 被 setup 替代
- beforeMount: 被 onBeforeMount 替代
- mounted: 被 onMounted 替代
- beforeUpdate: 被 onBeforeUpdate 替代
- updated: 被 onUpdated 替代
- beforeDestroy: 被 onBeforeUnmount 替代
- destroyed: 被 onUnmounted 替代

```vue
<script lang="ts" setup>
import {
  onBeforeMount,
  onBeforeUnmount,
  onBeforeUpdate,
  onMounted,
  onUnmounted,
  onUpdated,
} from "vue";

console.log("setup");

onBeforeMount(() => {
  console.log("onBeforeMount");
});

onMounted(() => {
  console.log("onMounted");
});

onBeforeUpdate(() => {
  console.log("onBeforeUpdate");
});

onUpdated(() => {
  console.log("onUpdated");
});

onBeforeUnmount(() => {
  console.log("onBeforeUnmount");
});

onUnmounted(() => {
  console.log("onUnmounted");
});
</script>
```
