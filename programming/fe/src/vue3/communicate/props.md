# 通过 props

1. 父组件

```html
<script lang="ts" setup>
  import Child from "./Child.vue";
  import { reactive } from "vue";

  // 传给子组件的数据
  let dataList = reactive([
    { id: 1, name: "John" },
    { id: 2, name: "Doe" },
  ]);

  // 传给子组件的函数, 让子组件调用
  const addData = (item) => {
    dataList.push(item);
    console.log(dataList);
  };
</script>

<template>
  <div>
    <!-- 向子组件传递props -->
    <Child :dataList="dataList" :addData="addData" />
  </div>
</template>

<style scoped></style>
```

2. 子组件

```html
<script lang="ts" setup>
  // 接收父组件的数据
  let { dataList, addData } = defineProps(["dataList", "addData"]);

  console.log(dataList);

  const add = () => {
    // 调用父组件提供的函数, 向父组件传值
    addData({ id: 3, name: "Tom" });
  };
</script>

<template>
  <div>
    <button @click="add">Add</button>
  </div>
</template>

<style scoped></style>
```
