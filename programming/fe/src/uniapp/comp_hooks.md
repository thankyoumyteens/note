# 组件生命周期钩子

uni-app 组件支持的生命周期，与 vue 标准组件的生命周期相同

- beforeMount 在挂载开始之前被调用
- mounted 挂载到实例上去之后调用 注意：此处并不能确定子组件被全部挂载，如果需要子组件完全挂载之后在执行操作可以使用 $nextTick
- beforeUpdate 数据更新时调用，发生在虚拟 DOM 打补丁之前 仅 H5 平台支持
- updated 由于数据更改导致的虚拟 DOM 重新渲染和打补丁，在这之后会调用该钩子 仅 H5 平台支持

```ts
import { onBeforeMount, onMounted } from "vue";

onBeforeMount(() => {
  console.log("index onBeforeMount");
});
onMounted(() => {
  console.log("index onMounted");
});
```
