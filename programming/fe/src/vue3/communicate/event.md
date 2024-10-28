# 自定义事件

1. 父组件

```html
<script lang="ts" setup>
  import Child from "./Child.vue";
  import { reactive } from "vue";

  let dataList = reactive([
    { id: 1, name: "John" },
    { id: 2, name: "Doe" },
  ]);

  const changeValue = (item) => {
    dataList.push(item);
    console.log(dataList);
  };
</script>

<template>
  <div>
    <!-- 监听子组件的自定义事件 -->
    <Child @changeValue="changeValue" />
  </div>
</template>

<style scoped></style>
```

2. 子组件

```html
<script lang="ts" setup>
  // 声明自定义事件
  const changeValueEvent = defineEmits(["changeValue"]);

  const add = () => {
    // 通过触发自定义事件向父组件传值
    changeValueEvent("changeValue", { id: 3, name: "Tom" });
  };
</script>

<template>
  <div>
    <button @click="add">Add</button>
  </div>
</template>

<style scoped></style>
```
